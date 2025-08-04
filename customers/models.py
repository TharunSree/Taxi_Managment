from django.db import models
from vehicles.models import Vehicle


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Trip-specific info, as requested
    coming_from = models.CharField(max_length=200, blank=True, null=True)
    from_location = models.CharField(max_length=200, blank=True, null=True)
    to_location = models.CharField(max_length=200, blank=True, null=True)
    vehicle_type_selected = models.CharField(
        max_length=10,
        choices=Vehicle.VehicleType.choices,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        ordering = ['name']
