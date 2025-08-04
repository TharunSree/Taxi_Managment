from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class StaffUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'email')

    def __init__(self, *args, **kwargs):
        super(StaffUserCreationForm, self).__init__(*args, **kwargs)
        # Apply the 'form-control' class to all fields, including inherited ones
        self.fields['username'].widget.attrs.update({'class': 'form-control'})

        # ADDED: Apply styling to the password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

        # Optional: Customize the help text for clarity
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Staff users should have this flag set
        if commit:
            user.save()
            # Automatically assign the new user to the 'Staff' group
            staff_group = Group.objects.get(name='Staff')
            user.groups.add(staff_group)
        return user

class StaffUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'groups', 'is_active')

    def __init__(self, *args, **kwargs):
        super(StaffUserChangeForm, self).__init__(*args, **kwargs)
        # Apply Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                 field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.SelectMultiple):
                 field.widget.attrs.update({'class': 'form-select', 'size': '4'})
            else:
                 field.widget.attrs.update({'class': 'form-control'})


class AdminPasswordResetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})