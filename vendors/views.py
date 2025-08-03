from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Vendor
from .forms import VendorForm


@login_required
def vendor_list_view(request):
    # Get the selected district from the URL query parameter
    selected_district = request.GET.get('district', '')

    # Get a list of all unique districts to populate the filter dropdown
    districts = Vendor.objects.values_list('district', flat=True).distinct().order_by('district')

    # Start with all vendors
    vendors = Vendor.objects.all()

    # If a district is selected, filter the queryset
    if selected_district:
        vendors = vendors.filter(district__iexact=selected_district)

    context = {
        'vendors': vendors,
        'districts': districts,
        'selected_district': selected_district,
        'title': 'Vendors'
    }
    return render(request, 'vendors/vendor_list.html', context)

@login_required
def vendor_add_view(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor added successfully!')
            return redirect('vendor_list')
    else:
        form = VendorForm()

    context = {
        'form': form,
        'title': 'Add Vendor'
    }
    return render(request, 'vendors/vendor_form.html', context)

@login_required
def vendor_update_view(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor updated successfully!')
            return redirect('vendor_list')
    else:
        form = VendorForm(instance=vendor)

    context = {
        'form': form,
        'title': 'Update Vendor'
    }
    return render(request, 'vendors/vendor_form.html', context)

@login_required
@permission_required('vendors.delete_vendors', raise_exception=True)
def vendor_delete_view(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        vendor.delete()
        messages.success(request, 'Vendor deleted successfully!')
        return redirect('vendor_list')

    context = {
        'vendor': vendor,
        'title': 'Delete Vendor'
    }
    return render(request, 'vendors/vendor_confirm_delete.html', context)

def vendors_by_district_api(request):
    district = request.GET.get('district')
    if district:
        vendor_list = Vendor.objects.filter(district__iexact=district).values('id', 'name')
    else:
        vendor_list = Vendor.objects.all().values('id', 'name')
    vendors = list(vendor_list)
    return JsonResponse(vendors, safe=False)