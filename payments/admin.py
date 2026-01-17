from django.contrib import admin
from payments.models import RentRecord, Payment

# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'rent_record',
        'amount',
        'payment_method',
        'reference',
        'received_by',
        'paid_at',
    )

    list_filter = ('payment_method', 'paid_at')
    search_fields = (
        'reference',
        'rent_record__tenancy__tenant__name'
    )

    readonly_fields = ('paid_at',)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('paid_at',)

@admin.register(RentRecord)
class RentRecordAdmin(admin.ModelAdmin):
    list_display = (
        'tenancy',
        'month',
        'year',
        'rent_amount',
        'total_paid',
        'balance_display',
        'status',
    )

    inlines = [PaymentInline]

    list_filter = ('status', 'year', 'month')
    search_fields = (
        'tenancy__tenant__name',
        'tenancy__unit__unit_number',
    )

    readonly_fields = (
        'total_paid',
        'status',
        'created_at',
    )

    def balance_display(self, obj):
        return obj.balance
    
    balance_display.short_description = '"Balance'