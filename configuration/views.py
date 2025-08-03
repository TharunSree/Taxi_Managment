from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import SiteConfiguration
from .forms import SiteConfigurationForm


# This test ensures only superusers can access the view
def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def site_settings_view(request):
    # Get the single settings instance
    config = SiteConfiguration.get_solo()

    if request.method == 'POST':
        form = SiteConfigurationForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site settings have been updated successfully!')
            return redirect('site_settings')
    else:
        form = SiteConfigurationForm(instance=config)

    context = {
        'form': form,
        'title': 'Site Settings'
    }
    return render(request, 'configuration/settings_form.html', context)