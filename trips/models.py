from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from customers.models import Customer
from vehicles.models import Vehicle
from vendors.models import Vendor


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Use the choices from the Vehicle model
    vehicle_type = models.CharField(max_length=10, choices=Vehicle.VehicleType.choices)
    vehicle_model = models.CharField(max_length=100, help_text="e.g., Innova, Swift Dzire")
    charges = models.DecimalField(max_digits=10, decimal_places=2)
    extra_charge_per_km = models.DecimalField(max_digits=10, decimal_places=2,
                                              help_text="Cost for each extra kilometer")

    def __str__(self):
        return f"{self.name} ({self.vehicle_type} - {self.vehicle_model})"


class Trip(models.Model):
    class TripStatus(models.TextChoices):
        UPCOMING = 'Upcoming', 'Upcoming'
        ON_GOING = 'On-going', 'On-going'
        COMPLETED = 'Completed', 'Completed'
        CANCELLED = 'Cancelled', 'Cancelled'

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='trips')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name='trips')
    trip_date = models.DateTimeField()
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, blank=True, null=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    advance_paid_date = models.DateField(blank=True, null=True)
    final_payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_payment_date = models.DateField(null=True, blank=True)
    vendor_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                       help_text="Amount to be paid to the vendor")
    vendor_advance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         help_text="Advance paid to the vendor")
    vendor_advance_date = models.DateField(blank=True, null=True)

    # remaining_amount can be calculated property
    @property
    def final_balance(self):
        # Calculate the new total price including extra distance
        extra_km_rate = 0
        if self.package and self.package.extra_charge_per_km is not None:
            extra_km_rate = self.package.extra_charge_per_km
        else:
            extra_km_rate = self.vehicle.price_per_km

        additional_cost = (self.additional_distance or 0) * extra_km_rate
        grand_total = self.total_price + additional_cost

        paid_amount = (self.advance_paid or 0) + (self.final_payment_amount or 0)

        return grand_total - paid_amount

    @property
    def agent_revenue(self):
        """Calculates the commission (Agent Revenue) for this trip."""
        if self.total_price and self.vendor_price:
            return self.total_price - self.vendor_price
        return Decimal('0.00')

    @property
    def remaining_amount(self):
        return self.total_price - self.advance_paid

    status = models.CharField(max_length=10, choices=TripStatus.choices, default=TripStatus.UPCOMING)

    # For trip finalization
    additional_distance = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trip for {self.customer.name} on {self.trip_date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-trip_date']


class Rating(models.Model):
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, related_name='rating')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='ratings')
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stars} stars for {self.vendor.name} on Trip #{self.trip.id}"
