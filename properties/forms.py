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

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['full_name', 'phone', 'email', 'national_id']

class TenantAssignmentForm(forms.ModelForm):
    class Meta:
        model = Tenancy
        fields = ['tenant', 'unit']
    
    def clean_unit(self):
        unit = self.cleaned_data['unit']
        if unit.status == Unit.OCCUPIED:
            raise forms.ValidationError("This unit is already occupied.")
        return unit