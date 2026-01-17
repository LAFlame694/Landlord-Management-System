from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from properties.models import Tenancy
from .models import RentRecord

# Create your views here.
@login_required
def rent_record_list(request, tenancy_id):
    tenancy = get_object_or_404(Tenancy, id=tenancy_id)

    # permission checks
    if request.user.is_landlord():
        if tenancy.unit.apartment.landlord != request.user:
            raise PermissionDenied
        
    if request.user.is_caretaker():
        if tenancy.unit.apartment.caretakers != request.user:
            raise PermissionDenied
    
    rent_records = (
        RentRecord.objects.filter(tenancy=tenancy).prefetch_related('payments').order_by('-year', '-month')
    )

    return render(request, 'payments/rent_record_list.html', {
        'tenancy': tenancy,
        'rent_records': rent_records
    })