from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    LANDLORD = 'LANDLORD'
    CARETAKER = 'CARETAKER'

    ROLE_CHOICES = [
        (LANDLORD, 'Landlord'),
        (CARETAKER, 'Caretaker'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    def is_landlord(self):
        return self.role == self.LANDLORD
    
    def is_caretaker(self):
        return self.role == self.CARETAKER