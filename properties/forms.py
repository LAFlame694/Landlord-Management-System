from django import forms
from .models import Apartment, Unit, Tenancy, Tenant

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['name', 'location', 'caretakers']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'caretakers': forms.Select(attrs={'class': 'form-control'}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_number', 'rent', 'status']
        widgets = {
            'unit_number': forms.TextInput(attrs={'placeholder': 'e.g. A12'}),
            'rent': forms.NumberInput(attrs={'placeholder': 'e.g. 15000'}),
        }

class TenancyForm(forms.ModelForm):
    class Meta:
        model = Tenancy
        fields = [
            'start_date',
            'end_date',
        ]

        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'end_date': forms.DateInput(attrs={'type':'date'}),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['full_name', 'phone', 'email', 'national_id']

        widgets = {
            'full_name': forms.TextInput(
                attrs={'placeholder': 'Full Name'}
            ),
            'phone': forms.TextInput(
                attrs={'placeholder': 'Phone Number'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Email Address'}
            ),
            'national_id': forms.TextInput(
                attrs={'placeholder': 'National ID'}
            ),
        }

class TenantAssignmentForm(forms.ModelForm):
    class Meta:
        model = Tenancy
        fields = ['tenant', 'unit']
    
    def clean_unit(self):
        unit = self.cleaned_data['unit']
        if unit.status == Unit.OCCUPIED:
            raise forms.ValidationError("This unit is already occupied.")
        return unit