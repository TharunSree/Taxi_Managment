import datetime
from django.utils import timezone

from django import forms
from .models import Trip, Package, Rating


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'customer', 'vehicle', 'trip_date', 'package', 'total_price', 'advance_paid', 'advance_paid_date',
            'customer_payment_option',
            'vendor_price', 'vendor_advance', 'vendor_advance_date','vendor_payment_option',
            'status', 'remarks'
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'package': forms.Select(attrs={'class': 'form-select'}),
            'trip_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'advance_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'advance_paid_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'vendor_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'vendor_advance': forms.NumberInput(attrs={'class': 'form-control'}),
            'vendor_advance_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'customer_payment_option': forms.Select(attrs={'class': 'form-select'}),
            'vendor_payment_option': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')
        self.fields['trip_date'].widget.attrs['min'] = today

    def clean_trip_date(self):
        trip_date = self.cleaned_data['trip_date']
        now = timezone.now()
        if trip_date < now:
            from django.core.exceptions import ValidationError
            raise ValidationError("Trip date cannot be in the past.")
        return trip_date


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name', 'vehicle_type', 'vehicle_model', 'charges', 'extra_charge_per_km']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'vehicle_model': forms.TextInput(attrs={'class': 'form-control'}),
            'charges': forms.NumberInput(attrs={'class': 'form-control'}),
            'extra_charge_per_km': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TripFinalizeForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['additional_distance', 'final_payment_amount', 'final_payment_date']
        widgets = {
            'additional_distance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 50'}),
            'final_payment_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'final_payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars', 'comment']
        widgets = {
            'stars': forms.HiddenInput(),  # Hidden input to store the selected rating
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
