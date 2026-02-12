from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.utils import landlord_required, caretaker_required
from datetime import date
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Value
from properties.models import Apartment, Unit, Tenancy
from payments.models import RentRecord
import calendar
from calendar import month_name
from django.db.models.functions import Coalesce
from django.db import transaction

# Create your views here.
@login_required
def home_redirect(request):
    user = request.user

    if user.is_landlord():
        return redirect('landlord_dashboard')
    elif user.is_caretaker():
        return redirect('caretaker_dashboard')
    
    # fallback
    return redirect('accounts:login')

def ensure_rent_records_for_month(landlord, year, month):
     """
    Ensure rent records exist for all tenancies that were active
    during the selected month.
    """
     first_day = date(year, month, 1)
     last_day = date(year, month, calendar.monthrange(year, month)[1])

     tenancies = Tenancy.objects.filter(
         unit__apartment__landlord=landlord
     ).select_related('unit')

     for tenancy in tenancies:
         # check if tenancy was active during this month
         started_before_month_end = tenancy.start_date <= last_day
         not_ended_before_month_start = (
             tenancy.end_date is None or tenancy.end_date >= first_day
         )

         if started_before_month_end and not_ended_before_month_start:
             
             # if rent record doesnt exist, create it
             RentRecord.objects.get_or_create(
                 tenancy=tenancy,
                 year=year,
                 month=month,
                 defaults={
                     'rent_amount': tenancy.unit.rent,
                     'total_paid': 0
                 }
             )

@login_required
@landlord_required
def landlord_dashboard(request):
    landlord = request.user

    today = date.today()
    current_year = today.year

    # FILTER: default to current month
    selected_month = int(request.GET.get('month', today.month))
    month_name = calendar.month_name[selected_month]

    ensure_rent_records_for_month(landlord, current_year, selected_month)

    active_tenancies = Tenancy.objects.filter(
        unit__apartment__landlord=request.user,
        is_active=True
    ).select_related(
        'tenant',
        'unit',
        'unit__apartment'
    )
    
    unpaid_tenants = []

    for tenancy in active_tenancies:

        rent_record = RentRecord.objects.filter(
            tenancy=tenancy,
            month=selected_month,
            year=current_year
        ).first()

        if rent_record:
            balance = rent_record.rent_amount - rent_record.total_paid

            if balance > 0:
                unpaid_tenants.append({
                    'tenant_name': f"{tenancy.tenant.full_name}",
                    'apartment': tenancy.unit.apartment.name,
                    'unit_number': tenancy.unit.unit_number,
                    'balance': balance,
                    'tenancy_id': tenancy.id,
                })

    # Apartments and units
    apartments = Apartment.objects.filter(landlord=landlord)
    total_apartments = apartments.count()

    units = Unit.objects.filter(apartment__landlord=landlord)
    total_units = units.count()

    # Occupancy
    occupied_units = units.filter(
        tenancies__is_active=True
    ).distinct().count()

    vacant_units = total_units - occupied_units

    # Rent records for selected month
    rent_records = RentRecord.objects.filter(
        tenancy__unit__apartment__landlord=landlord,
        year=current_year,
        month=selected_month
    )

    expected_rent = rent_records.aggregate(
        total=Sum('rent_amount')
    )['total'] or 0

    collected_rent = rent_records.aggregate(
        total=Sum('total_paid')
    )['total'] or 0

    outstanding_balance = expected_rent - collected_rent

    return render(request, 'dashboards/landlord_dashboard.html', {
        'total_apartments': total_apartments,
        'total_units': total_units,
        'occupied_units': occupied_units,
        'vacant_units': vacant_units,
        'expected_rent': expected_rent,
        'collected_rent': collected_rent,
        'outstanding_balance': outstanding_balance,
        'current_year': current_year,
        'selected_month': selected_month,
        'month_name': month_name,
        'unpaid_tenants': unpaid_tenants,
    })

@login_required
@caretaker_required
def caretaker_dashboard(request):
    caretaker = request.user

    today = date.today()
    current_year = today.year
    current_month = today.month

    apartments = Apartment.objects.filter(caretakers=caretaker)

    # unpaid rent records for current month
    unpaid_rent_records = RentRecord.objects.filter(
        tenancy__unit__apartment__caretakers=caretaker,
        year=current_year,
        month=current_month,
        rent_amount__gt=F('total_paid')
    ).select_related(
        'tenancy',
        'tenancy__tenant',
        'tenancy__unit',
        'tenancy__unit__apartment'
    )

    return render(request, 'dashboards/caretaker_dashboard.html', {
        'apartments': apartments,
        'unpaid_rent_records': unpaid_rent_records,
        'current_month': current_month,
        'current_year': current_year,
    })

"""
passwords:
admin: osama694
kamaa: kamaa694
"""