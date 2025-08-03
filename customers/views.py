from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Customer
from .forms import CustomerForm


# This is the list view we already created
@login_required
def customer_list_view(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers,
        'title': 'Customers'
    }
    return render(request, 'customers/customer_list.html', context)


# ADD THIS NEW VIEW
@login_required
def customer_add_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()

    context = {
        'form': form,
        'title': 'Add Customer'
    }
    return render(request, 'customers/customer_form.html', context)


@login_required
def customer_update_view(request, pk):
    # Fetch the specific customer object, or return a 404 error if not found
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        # Pass the instance to the form to update it
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_list')
    else:
        # Pre-populate the form with the existing customer's data
        form = CustomerForm(instance=customer)

    context = {
        'form': form,
        'title': 'Update Customer'  # Dynamic title for the template
    }
    return render(request, 'customers/customer_form.html', context)


@login_required
@permission_required('customers.delete_customer', raise_exception=True)
def customer_delete_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('customer_list')

    context = {
        'customer': customer,
        'title': 'Delete Customer'
    }
    return render(request, 'customers/customer_confirm_delete.html', context)


@login_required
def customer_add_ajax_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            # Return a success response with the new customer's details
            return JsonResponse({
                'success': True,
                'customer': {
                    'id': customer.id,
                    'name': str(customer)  # Uses the __str__ method from the model
                }
            })
        else:
            # Return form errors if validation fails
            return JsonResponse({'success': False, 'errors': form.errors})
    # Redirect if accessed via GET
    return redirect('customer_list')
