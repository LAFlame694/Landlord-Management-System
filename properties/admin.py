from django.contrib import admin
from .models import Apartment, Unit, Tenancy, Tenant

# Register your models here.
@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'landlord', 'caretakers')
    list_filter = ('landlord',)
    search_fields = ('name', 'location')

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'apartment', 'rent', 'status')
    list_filter = ('status', 'apartment')

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email')
    search_fields = ('full_name', 'phone')

@admin.register(Tenancy)
class TenancyAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'unit', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)