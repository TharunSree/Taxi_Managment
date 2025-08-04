from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, DecimalField
from datetime import datetime
from weasyprint import HTML

from django.template.loader import render_to_string

from trips.models import Trip
from django.shortcuts import get_object_or_404
from decimal import Decimal


@login_required
def trip_report_view(request):
    # Get filter parameters from the form submission
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Start with all trips
    trips = Trip.objects.select_related('customer', 'vehicle', 'package').all()

    # Apply filters if dates are provided
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        trips = trips.filter(trip_date__date__gte=start_date)

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        trips = trips.filter(trip_date__date__lte=end_date)

    # Calculate totals from the filtered trips
    summary = trips.aggregate(
        total_trips=Count('id'),
        total_revenue=Sum('total_price'),
        total_agent_revenue=Sum(F('total_price') - F('vendor_price'), output_field=DecimalField()),
        total_advance=Sum('advance_paid')
    )

    # Serialize the queryset into a list of dictionaries for JavaScript
    trip_data_for_js = [
        {
            'id': trip.id,
            'customer': trip.customer.name,
            'vehicle': str(trip.vehicle),
            'trip_date': trip.trip_date.strftime("%d %b %Y, %I:%M %p"),
            'status': trip.get_status_display(),
            'advance_paid': float(trip.advance_paid) if trip.advance_paid else 0.0,
            'vendor_price': float(trip.vendor_price) if trip.vendor_price else 0.0,
            'vendor_advance': float(trip.vendor_advance) if trip.vendor_advance else 0.0,
            'total_price': float(trip.total_price) if trip.total_price else 0.0,
            'agent_revenue': float(trip.agent_revenue) if trip.agent_revenue else 0.0,
        }
        for trip in trips
    ]

    context = {
        # Keep the `trips` variable for the summary block
        'trips': trips,
        'summary': summary,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'title': 'Trip Report',
        'trip_data_for_js': trip_data_for_js,
    }
    return render(request, 'reports/trip_report.html', context)


@login_required
def generate_bill_view(request, pk):
    trip = get_object_or_404(Trip.objects.select_related('customer', 'vehicle', 'package', 'vehicle__vendor'), pk=pk)

    # Calculate financial details
    base_price = trip.total_price
    additional_cost = Decimal('0.00')

    if trip.additional_distance and trip.additional_distance > 0:
        if trip.package and trip.package.extra_charge_per_km is not None:
            extra_km_rate = trip.package.extra_charge_per_km
        else:
            extra_km_rate = trip.vehicle.price_per_km

        additional_cost = trip.additional_distance * extra_km_rate
        base_price -= additional_cost  # Adjust base price to what it was before finalization

    grand_total = base_price + additional_cost
    balance_due = grand_total - (trip.advance_paid or 0) - (trip.final_payment_amount or 0)

    context = {
        'trip': trip,
        'base_price': base_price,
        'additional_cost': additional_cost,
        'grand_total': grand_total,
        'balance_due': balance_due,
        'title': f'Invoice for Trip #{trip.id}'
    }
    return render(request, 'reports/invoice.html', context)


@login_required
def generate_customer_pdf(request, pk):
    trip = get_object_or_404(Trip.objects.select_related('customer', 'vehicle'), pk=pk)
    html_string = render_to_string('reports/pdfs/customer_confirmation.html', {'trip': trip})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="customer_confirmation_{trip.id}.pdf"'

    HTML(string=html_string).write_pdf(response)
    return response


@login_required
def generate_vendor_pdf(request, pk):
    trip = get_object_or_404(Trip.objects.select_related('customer', 'vehicle', 'vehicle__vendor'), pk=pk)
    html_string = render_to_string('reports/pdfs/vendor_confirmation.html', {'trip': trip})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vendor_order_{trip.id}.pdf"'

    HTML(string=html_string).write_pdf(response)
    return response
