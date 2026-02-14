from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from datetime import date
from decimal import Decimal

from properties.models import Tenancy
from .models import RentRecord, Payment

# Create your views here.
@login_required
def record_payment(request, record_id):
    rent_record = get_object_or_404(RentRecord, id=record_id)
    tenancy = rent_record.tenancy

    # Permissions
    if request.user.is_landlord():
        if tenancy.unit.apartment.landlord != request.user:
            raise PermissionDenied
        
    if request.user.is_caretaker():
        if tenancy.unit.apartment.caretakers != request.user:
            raise PermissionDenied
    
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        method = request.POST.get('payment_method')
        reference = request.POST.get('reference')

        # prevent overpayment
        if amount > rent_record.balance:
            return render(request, 'payments/record_payment.html', {
                'rent_record': rent_record,
                'error': 'Payment exceeds balance.'
            })
        
        Payment.objects.create(
            rent_record=rent_record,
            amount=amount,
            payment_method=method,
            reference=reference,
            received_by=request.user
        )

        return redirect('rent_record_list', tenancy_id=tenancy.id)
    
    return render(request, 'payments/record_payment.html', {
        'rent_record': rent_record
    })

@login_required
def rent_record_list(request, tenancy_id):
    tenancy = get_object_or_404(Tenancy, id=tenancy_id)

    today = date.today()

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