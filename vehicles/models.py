from django.db import models
from vendors.models import Vendor

class Vehicle(models.Model):
    class VehicleType(models.TextChoices):
        SEDAN = 'Sedan', 'Sedan'
        HATCHBACK = 'Hatchback', 'Hatchback'
        SUV = 'SUV', 'SUV'
        VAN = 'Van', 'Van'
        MINIBUS = 'Minibus', 'Minibus'

    number = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=10, choices=VehicleType.choices)
    make = models.CharField(max_length=50)  # e.g., Toyota
    model = models.CharField(max_length=50)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vehicles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price_per_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=20.00,
        help_text="Default price per extra kilometer for non-package trips."
    )

    def __str__(self):
        return f"{self.number} - {self.type} ({self.vendor.name})"

    class Meta:
        ordering = ['-created_at']