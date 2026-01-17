from django.db import models
from properties.models import Tenancy
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class RentRecord(models.Model):
    tenancy = models.ForeignKey(
        Tenancy,
        on_delete=models.CASCADE,
        related_name='rent_records'
    )

    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(12)
        ]
    )

    rent_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('UNPAID', 'Unpaid'),
            ('PARTIAL', 'Partially Paid'),
            ('PAID', 'Paid'),
        ],
        default='UNPAID'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tenancy', 'year', 'month')
        ordering = ['-year', '-month']
        indexes = [
            models.Index(fields=['tenancy', 'year', 'month']),
            models.Index(fields=['status']),
        ]

    @property
    def balance(self):
        return self.rent_amount - self.total_paid
    
    @property
    def is_fully_paid(self):
        return self.balance <= 0
    
    def recalculate_payment_status(self):
        """Single source of truth"""
        total = self.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or 0

        self.total_paid = total

        if total == 0:
            self.status = 'UNPAID'
        elif total < self.rent_amount:
            self.status = 'PARTIAL'
        else:
            self.status = 'PAID'

        self.save(update_fields=['total_paid', 'status'])
    
    def __str__(self):
        return f"{self.tenancy.tenant.full_name} - {self.month}/{self.year}"
    
class Payment(models.Model):
    rent_record = models.ForeignKey(
        RentRecord,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('CASH', 'Cash'),
            ('MPESA', 'M-Pesa'),
            ('BANK', 'Bank'),
        ]
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    received_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True
    )

    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.payment_method}"