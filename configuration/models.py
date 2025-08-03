from django.db import models
from solo.models import SingletonModel

class SiteConfiguration(SingletonModel):
    email_host = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., smtp.gmail.com")
    email_port = models.PositiveIntegerField(default=587, help_text="e.g., 587 for TLS")
    email_host_user = models.EmailField(blank=True, null=True, help_text="The 'from' email address")
    email_host_password = models.CharField(max_length=100, blank=True, null=True, help_text="Use an 'App Password' for services like Gmail")
    email_use_tls = models.BooleanField(default=True)
    default_from_email = models.EmailField(blank=True, null=True, help_text="e.g., Aronee <noreply@gminitours.com>")

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"