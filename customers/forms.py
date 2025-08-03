from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'coming_from', 'from_location', 'to_location',
                  'vehicle_type_selected']

        # Add Bootstrap classes to the form widgets for consistent styling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'coming_from': forms.TextInput(attrs={'class': 'form-control'}),
            'from_location': forms.TextInput(attrs={'class': 'form-control'}),
            'to_location': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type_selected': forms.Select(attrs={'class': 'form-select'}),
        }