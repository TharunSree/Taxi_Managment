import json

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse

from customers.forms import CustomerForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from vehicles.models import Vehicle
from vendors.models import Vendor
from .models import Trip, Package
from .forms import TripForm, PackageForm, TripFinalizeForm, RatingForm


@login_required
def trip_list_view(request):
    # Get status from URL query parameter
    status_filter = request.GET.get('status', '')

    trips = Trip.objects.select_related('customer', 'vehicle', 'vehicle__vendor').all()

    # Apply filter if a status is provided
    if status_filter:
        trips = trips.filter(status=status_filter)

    context = {
        'trips': trips,
        'title': 'Trips'
    }
    return render(request, 'trips/trip_list.html', context)


@login_required
def trip_add_view(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save()
            if trip.customer.email:
                subject = f'Trip Confirmed: Aronee Booking #{trip.id}'
                html_message = render_to_string('emails/trip_confirmation.html', {'trip': trip})
                send_mail(
                    subject, '',
                    settings.DEFAULT_FROM_EMAIL,
                    [trip.customer.email],
                    html_message=html_message
                )
            messages.success(request, 'Trip created successfully!')
            return redirect('trip_list')
    else:
        form = TripForm()
    packages = Package.objects.all()
    # Pass only the base charges for auto-filling the price

    package_prices = {str(p.id): str(p.charges) for p in packages}
    districts = Vendor.objects.values_list('district', flat=True).distinct().order_by('district')
    vehicle_types = Vehicle.VehicleType.choices
    context = {
        'form': form,
        'title': 'Create a New Trip',
        'package_prices_json': json.dumps(package_prices),
        'customer_form': CustomerForm(),
        'districts': districts,
        'vehicle_types': vehicle_types,
    }
    return render(request, 'trips/trip_form.html', context)


@login_required
def trip_update_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trip updated successfully!')
            return redirect('trip_list')
    else:
        form = TripForm(instance=trip)
    packages = Package.objects.all()
    # Pass only the base charges for auto-filling the price
    districts = Vendor.objects.values_list('district', flat=True).distinct().order_by('district')
    vehicle_types = Vehicle.VehicleType.choices
    package_prices = {str(p.id): str(p.charges) for p in packages}
    context = {
        'form': form,
        'title': 'Update Trip',
        'package_prices_json': json.dumps(package_prices),
        'customer_form': CustomerForm(),
        'districts': districts,
        'vehicle_types': vehicle_types,
    }
    return render(request, 'trips/trip_form.html', context)


@login_required
def trip_cancel_view(request, pk):
    trip = get_object_or_404(Trip.objects.select_related('customer'), pk=pk)

    if request.method == 'POST':
        trip.status = 'Cancelled'
        trip.save()

        # --- Send Cancellation Email ---
        if trip.customer.email:
            subject = f'Trip Cancelled: Aronee Booking #{trip.id}'
            html_message = render_to_string('emails/trip_cancellation.html', {'trip': trip})
            send_mail(
                subject,
                '',  # Plain text message (optional)
                settings.DEFAULT_FROM_EMAIL,
                [trip.customer.email],
                html_message=html_message,
                fail_silently=False  # Set to True in production if you want to ignore errors
            )

        messages.success(request, 'Trip has been successfully cancelled.')
        return redirect('trip_list')

    context = {
        'trip': trip,
        'title': 'Confirm Cancellation'
    }
    return render(request, 'trips/trip_confirm_cancel.html', context)


@login_required
def package_list_view(request):
    packages = Package.objects.all()
    context = {
        'packages': packages,
        'title': 'Trip Packages'
    }
    return render(request, 'trips/packages/package_list.html', context)


@login_required
def package_add_view(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package created successfully!')
            return redirect('package_list')
    else:
        form = PackageForm()
    context = {
        'form': form,
        'title': 'Create New Package'
    }
    return render(request, 'trips/packages/package_form.html', context)


@login_required
def package_update_view(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        form = PackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package updated successfully!')
            return redirect('package_list')
    else:
        form = PackageForm(instance=package)
    context = {
        'form': form,
        'title': 'Update Package'
    }
    return render(request, 'trips/packages/package_form.html', context)


@login_required
@permission_required('vendors.delete_package', raise_exception=True)
def package_delete_view(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'Package deleted successfully!')
        return redirect('package_list')
    context = {
        'package': package,
        'title': 'Delete Package'
    }
    return render(request, 'trips/packages/package_confirm_delete.html', context)


@login_required
def trip_finalize_view(request, pk):
    trip = get_object_or_404(Trip.objects.select_related('package', 'vehicle'), pk=pk)

    # Determine the rate for extra kilometers
    if trip.package and trip.package.extra_charge_per_km is not None:
        extra_km_rate = trip.package.extra_charge_per_km
    else:
        extra_km_rate = trip.vehicle.price_per_km

    if request.method == 'POST':
        form = TripFinalizeForm(request.POST, instance=trip)
        if form.is_valid():
            finalized_trip = form.save(commit=False)

            # Calculate final total price
            additional_distance = finalized_trip.additional_distance or 0
            additional_cost = additional_distance * extra_km_rate
            finalized_trip.total_price += additional_cost

            finalized_trip.status = 'Completed'
            finalized_trip.save()

            messages.success(request, f'Trip for {trip.customer.name} has been completed and finalized!')
            return redirect('trip_list')
    else:
        form = TripFinalizeForm(instance=trip)

    context = {
        'form': form,
        'trip': trip,
        'extra_km_rate': extra_km_rate,
        'title': 'Finalize Trip'
    }
    return render(request, 'trips/trip_finalize_form.html', context)


@login_required
def add_rating_view(request, pk):
    trip = get_object_or_404(Trip.objects.select_related('vehicle__vendor'), pk=pk)

    # Prevent rating if the trip is not completed or already rated
    if trip.status != 'Completed' or hasattr(trip, 'rating'):
        messages.error(request, 'This trip cannot be rated.')
        return redirect('trip_list')

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.trip = trip
            rating.vendor = trip.vehicle.vendor  # Get the vendor from the trip's vehicle
            rating.save()
            messages.success(request, 'Rating submitted successfully!')
            return redirect('trip_list')
    else:
        form = RatingForm()

    context = {
        'form': form,
        'trip': trip,
        'title': 'Rate Trip'
    }
    return render(request, 'trips/trip_rate_form.html', context)


def trip_feed_view(request):
    """
    Provides a daily summary of trips as a JSON feed for the FullCalendar.
    """
    # Group trips by date and get the count for each day
    daily_counts = Trip.objects.annotate(
        date=TruncDate('trip_date')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    events = []
    for daily_summary in daily_counts:
        events.append({
            # The title will now be the total count
            'title': f"Total Trips: {daily_summary['count']}",
            'start': daily_summary['date'].isoformat(),
            'allDay': True,  # This displays the event neatly at the top of the day cell
        })

    return JsonResponse(events, safe=False)
