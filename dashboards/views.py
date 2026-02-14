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
from django.contrib import messages
from django.db import transaction
from django.db import models

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

from datetime import date
from django.db import transaction

def ensure_rent_records_for_month(landlord, year, month):
    """
    Strict Accounting Mode:
    - Only generate records for past or current month
    - Never generate future records
    - Only for tenancies active during that month
    """

    today = date.today()

    # 🚫 Do not allow future generation
    if (year, month) > (today.year, today.month):
        return

    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])

    tenancies = Tenancy.objects.filter(
        unit__apartment__landlord=landlord,
        start_date__lte=last_day
    ).filter(
        models.Q(end_date__isnull=True) |
        models.Q(end_date__gte=first_day)
    ).select_related('unit')

    existing_records = set(
        RentRecord.objects.filter(
            tenancy__in=tenancies,
            year=year,
            month=month
        ).values_list('tenancy_id', flat=True)
    )

    records_to_create = []

    for tenancy in tenancies:
        if tenancy.id not in existing_records:
            records_to_create.append(
                RentRecord(
                    tenancy=tenancy,
                    year=year,
                    month=month,
                    rent_amount=tenancy.unit.rent,
                    total_paid=0,
                )
            )

    if records_to_create:
        with transaction.atomic():
            RentRecord.objects.bulk_create(records_to_create)

@login_required
@landlord_required
def landlord_dashboard(request):
    landlord = request.user

    today = date.today()
    current_year = today.year

    selected_month = int(request.GET.get('month', today.month))
    month_name = calendar.month_name[selected_month]

    # ensure records exist for valid tenancies
    ensure_rent_records_for_month(landlord, current_year, selected_month)

    rent_records = (
        RentRecord.objects
        .filter(
            tenancy__unit__apartment__landlord=landlord,
            year=current_year,
            month=selected_month
        )
        .select_related(
            'tenancy',
            'tenancy__tenant',
            'tenancy__unit',
            'tenancy__unit__apartment'
        )
        .annotate(
            computed_balance=ExpressionWrapper(
                F('rent_amount') - F('total_paid'),
                output_field=DecimalField()
            )
        )
    )

    unpaid_records = rent_records.filter(computed_balance__gt=0)

    unpaid_tenants = [
        {
            'tenant_name': record.tenancy.tenant.full_name,
            'apartment': record.tenancy.unit.apartment.name,
            'unit_number': record.tenancy.unit.unit_number,
            'balance': record.computed_balance,
            'tenancy_id': record.tenancy.id,
        }
        for record in unpaid_records
    ]

    totals = rent_records.aggregate(
        expected=Coalesce(
            Sum('rent_amount'),
            Value(0),
            output_field=DecimalField()
        ),
        collected=Coalesce(
            Sum('total_paid'),
            Value(0),
            output_field=DecimalField()
        )
    )

    expected_rent = totals['expected']
    collected_rent = totals['collected']
    outstanding_balance = expected_rent - collected_rent

    apartments = Apartment.objects.filter(landlord=landlord)
    total_apartments = apartments.count()

    units = Unit.objects.filter(apartment__landlord=landlord)
    total_units = units.count()

    occupied_units = units.filter(
        tenancies__is_active=True
    ).distinct().count()

    vacant_units = total_units - occupied_units

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
@landlord_required
def landlord_rent_reports(request):
    landlord = request.user

    today = date.today()
    current_year = today.year
    current_month = today.month

    apartments = Apartment.objects.filter(
        landlord=landlord
    ).order_by('name')

    if not apartments.exists():
        return render(request, 'dashboard/landlord_rent_reports.html', {
            'apartments': apartments,
            'rent_records': [],
        })
    
    selected_year = int(request.GET.get('year', current_year))
    selected_month = int(request.GET.get('month', current_month))

    selected_apartment_id = request.GET.get(
        'apartment',
        apartments.first().id
    )

    selected_apartment = apartments.filter(
        id=selected_apartment_id
    ).first()

    # Ensure rent records exist for valid tenancies
    ensure_rent_records_for_month(
        landlord,
        selected_year,
        selected_month
    )

    # RENT RECORD QUERY
    rent_records = RentRecord.objects.filter(
        tenancy__unit__apartment=selected_apartment,
        year=selected_year,
        month=selected_month
    ).select_related(
        'tenancy',
        'tenancy__tenant',
        'tenancy__unit'
    ).annotate(
        computed_balance=ExpressionWrapper(
            F('rent_amount') - F('total_paid'),
            output_field=DecimalField()
        )
    ).order_by('tenancy__unit__unit_number')

    # SUMMERY
    totals = rent_records.aggregate(
        expected=Coalesce(
            Sum('rent_amount'),
            Value(0),
            output_field=DecimalField()
        ),
        collected=Coalesce(
            Sum('total_paid'),
            Value(0),
            output_field=DecimalField()
        )
    )

    expected_rent = totals.get('expected',0)
    collected_rent = totals.get('collected',0)

    outstanding_balance = expected_rent - collected_rent

    collection_rate = 0
    if expected_rent > 0:
        collection_rate = round(
            (collected_rent / expected_rent) * 100, 2
        )

    return render(request, 'dashboards/landlord_rent_reports.html', {
        'apartments': apartments,
        'selected_apartment': selected_apartment,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'month_name': calendar.month_name[selected_month],
        'rent_records': rent_records,
        'expected_rent': expected_rent,
        'collected_rent': collected_rent,
        'outstanding_balance': outstanding_balance,
        'collection_rate': collection_rate,
        'current_year': current_year,
        'year_range': range(current_year - 3, current_year + 2),
        'months': [
            (i, calendar.month_name[i])
            for i in range(1, 13)
        ],
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