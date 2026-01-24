from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.utils import landlord_required, caretaker_required
from .models import Apartment, Unit, Tenancy, Tenant
from .forms import ApartmentForm, UnitForm, TenantForm, TenantAssignmentForm
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Count

# Create your views here.
@login_required
def assign_tenant(request, unit_id):

    if not (request.user.is_landlord() or request.user.is_caretaker()):
        raise PermissionDenied

    unit = get_object_or_404(Unit, id=unit_id)
    apartment = unit.apartment

    # LANDLORD: must own the apartment
    if request.user.is_landlord():
        if apartment.landlord != request.user:
            raise PermissionDenied

    # CARETAKER: must manage the apartment
    if request.user.is_caretaker():
        if apartment.caretakers != request.user:
            raise PermissionDenied
    
    # Prevent assigning to occupied unit
    if unit.status == Unit.OCCUPIED:
        raise PermissionDenied("This unit is already occupied.")

    tenant_form = TenantForm()

    if request.method == 'POST':
        tenant_form = TenantForm(request.POST)

        if tenant_form.is_valid():
            tenant = tenant_form.save()

            Tenancy.objects.create(
                tenant=tenant,
                unit=unit,
                is_active=True
            )

            unit.status = Unit.OCCUPIED
            unit.save()

            return redirect('apartment_units', apartment_id=apartment.id)
    
    return render(request, 'properties/assign_tenant.html', {
        'tenant_form': tenant_form,
        'unit': unit
    })

@login_required
def vacate_tenant(request, tenancy_id):
    tenancy = Tenancy.objects.get(id=tenancy_id, is_active=True)

    # permission check
    if request.user.is_caretaker():
        if tenancy.unit.apartment not in request.user.assigned_apartments.all():
            raise PermissionDenied
    
    tenancy.is_active = False
    tenancy.end_date = timezone.now()
    tenancy.save()

    unit = tenancy.unit
    unit.status = 'VACANT'
    unit.save()

    return redirect('caretaker_dashboard')

@login_required
@landlord_required
def unit_create(request, apartment_id):
    apartment = get_object_or_404(
        Apartment,
        id=apartment_id,
        landlord=request.user
    )

    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.apartment = apartment
            unit.save()
            return redirect('apartment_units', apartment_id=apartment.id)
    else:
        form = UnitForm()

    return render(request, 'properties/unit_form.html', {
        'form': form,
        'apartment': apartment
    })

# list units per apartment
@login_required
def apartment_units(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    # Landlord access
    if request.user.is_landlord():
        if apartment.landlord != request.user:
            raise PermissionDenied

    # Caretaker access
    elif request.user.is_caretaker():
        if apartment.caretakers != request.user:
            raise PermissionDenied

    else:
        raise PermissionDenied

    units = apartment.units.prefetch_related('tenancies')

    return render(request, 'properties/unit_list.html', {
        'apartment': apartment,
        'units': units
    })

@login_required
@landlord_required
def apartment_list(request):
    apartments = (
        Apartment.objects
        .filter(landlord=request.user)
        .annotate(total_units=Count('units'))
    )

    return render(request, 'properties/apartment_list.html', {
        'apartments': apartments
    })

@login_required
@landlord_required
def apartment_create(request):
    if request.method == 'POST':
        form = ApartmentForm(request.POST)
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.landlord = request.user
            apartment.save()
            form.save_m2m()
            return redirect('apartment_list')
    else:
        form = ApartmentForm()
    
    return render(request, 'properties/apartment_form.html', {
        'form': form
    })

@login_required
@landlord_required
def apartment_edit(request, pk):
    apartment = get_object_or_404(
        Apartment,
        pk=pk,
        landlord = request.user
    )

    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            form.save()
            return redirect('apartment_list')
    else:
        form = ApartmentForm(instance=apartment)
    
    return render(request, 'properties/apartment_form.html', {
        'form': form
    })