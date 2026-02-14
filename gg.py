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