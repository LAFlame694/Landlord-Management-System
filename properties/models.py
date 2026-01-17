from django.db import models
from accounts.models import User
from django.utils.timezone import now

# Create your models here.
class Apartment(models.Model):
    landlord = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='apartments',
        limit_choices_to={'role': User.LANDLORD}
    )

    caretakers = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='apartments_managed',
        limit_choices_to={'role': User.CARETAKER}
    )

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.location}"

class Unit(models.Model):
    VACANT = 'VACANT'
    OCCUPIED = 'OCCUPIED'

    STATUS_CHOICES = [
        (VACANT, 'Vacant'),
        (OCCUPIED, 'Occupied'),
    ]

    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='units'
    )

    unit_number = models.CharField(max_length=20)
    rent = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=VACANT
    )

    @property
    def is_occupied(self):
        return self.tenancies.filter(is_active=True).exists()
    
    @property
    def active_tenancy(self):
        return self.tenancies.filter(is_active=True).first()

    def __str__(self):
        return f"{self.apartment.name} - {self.unit_number}"


class Tenant(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    national_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Tenancy(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name='tenancies'
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name='tenancies'
    )

    start_date = models.DateField(default=now)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['unit'],
                condition=models.Q(is_active=True),
                name='only_one_active_tenancy_per_unit'
            )
        ]
    
    def __str__(self):
        return f"{self.tenant} → {self.unit}"