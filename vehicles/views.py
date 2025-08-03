from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from vendors.models import Vendor
from .models import Vehicle
from .forms import VehicleForm


@login_required
def vehicle_list_view(request):
    selected_district = request.GET.get('district', '')
    selected_type = request.GET.get('type', '')

    # Data for the filter dropdowns
    districts = Vendor.objects.values_list('district', flat=True).distinct().order_by('district')
    vehicle_types = Vehicle.VehicleType.choices

    # Start with all vehicles
    vehicles = Vehicle.objects.select_related('vendor').all()

    # Apply filters
    if selected_district:
        vehicles = vehicles.filter(vendor__district__iexact=selected_district)

    if selected_type:
        vehicles = vehicles.filter(type=selected_type)

    context = {
        'vehicles': vehicles,
        'districts': districts,
        'vehicle_types': vehicle_types,
        'selected_district': selected_district,
        'selected_type': selected_type,
        'title': 'Vehicles'
    }
    return render(request, 'vehicles/vehicle_list.html', context)

@login_required
def vehicle_add_view(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('vehicle_list')
    else:
        form = VehicleForm()

    context = {
        'form': form,
        'title': 'Add Vehicle'
    }
    return render(request, 'vehicles/vehicle_form.html', context)

@login_required
def vehicle_update_view(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)

    context = {
        'form': form,
        'title': 'Update Vehicle'
    }
    return render(request, 'vehicles/vehicle_form.html', context)

@login_required
@permission_required('vehicles.delete_vehicles', raise_exception=True)
def vehicle_delete_view(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('vehicle_list')

    context = {
        'vehicle': vehicle,
        'title': 'Delete Vehicle'
    }
    return render(request, 'vehicles/vehicle_confirm_delete.html', context)


def vehicles_by_vendor_api(request):
    vendor_id = request.GET.get('vendor_id')
    vehicle_type = request.GET.get('type')
    district = request.GET.get('district')

    print(f"API called with: vendor_id={vendor_id}, type={vehicle_type}, district={district}")  # Debug log

    # Start with all vehicles
    vehicles = Vehicle.objects.select_related('vendor')

    # Filter by vendor if provided
    if vendor_id:
        vehicles = vehicles.filter(vendor_id=vendor_id)
        print(f"Filtered by vendor_id: {vehicles.count()} vehicles")  # Debug log
    # Filter by district if provided (and no specific vendor selected)
    elif district:
        vehicles = vehicles.filter(vendor__district__iexact=district)
        print(f"Filtered by district: {vehicles.count()} vehicles")  # Debug log

    # Filter by vehicle type if provided
    if vehicle_type:
        vehicles = vehicles.filter(type=vehicle_type)
        print(f"After type filter: {vehicles.count()} vehicles")  # Debug log

    # Format the data for the dropdown
    vehicle_list = []
    for v in vehicles:
        vehicle_list.append({
            'id': v.id,
            'name': f"{v.number} - {v.make} {v.model} ({v.vendor.name})"
        })

    print(f"Returning {len(vehicle_list)} vehicles")  # Debug log
    return JsonResponse(vehicle_list, safe=False)