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
            balance=ExpressionWrapper(
                F('rent_amount') - F('total_paid'),
                output_field=DecimalField()
            )
        )
    )

    unpaid_records = rent_records.filter(balance__gt=0)

    unpaid_tenants = [
        {
            'tenant_name': record.tenancy.tenant.full_name,
            'apartment': record.tenancy.unit.apartment.name,
            'unit_number': record.tenancy.unit.unit_number,
            'balance': record.balance,
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
