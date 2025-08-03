from django import forms
from .models import SiteConfiguration

class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = [
            'email_host', 'email_port', 'email_host_user',
            'email_host_password', 'email_use_tls', 'default_from_email'
        ]
        widgets = {
            'email_host': forms.TextInput(attrs={'class': 'form-control'}),
            'email_port': forms.NumberInput(attrs={'class': 'form-control'}),
            'email_host_user': forms.EmailInput(attrs={'class': 'form-control'}),
            'email_host_password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
            'email_use_tls': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'default_from_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }