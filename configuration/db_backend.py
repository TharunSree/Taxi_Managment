from django.core.mail.backends.smtp import EmailBackend as SmtpEmailBackend
from .models import SiteConfiguration


class DbEmailBackend(SmtpEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        # First, let the parent class initialize with any default
        # or settings.py values.
        super().__init__(fail_silently=fail_silently, **kwargs)

        # Now, get our configuration from the database
        try:
            config = SiteConfiguration.get_solo()

            # Override the connection attributes with our database values
            # only if they have been set in the admin.
            if config.email_host:
                self.host = config.email_host
            if config.email_port:
                self.port = config.email_port
            if config.email_host_user:
                self.username = config.email_host_user
            if config.email_host_password:
                self.password = config.email_host_password
            if config.email_use_tls is not None:
                self.use_tls = config.email_use_tls

        except SiteConfiguration.DoesNotExist:
            # If the config object hasn't been created in the admin yet,
            # just use the default settings and don't raise an error.
            pass