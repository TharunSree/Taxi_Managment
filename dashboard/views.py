from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Sum, Avg, F, DecimalField
from django.db.models.functions import TruncDay, TruncMonth, TruncDate
from django.http import JsonResponse
from datetime import timedelta

# Import all necessary models
from vendors.models import Vendor
from customers.models import Customer
from trips.models import Trip


@login_required
def dashboard_view(request):
    # --- WIDGET DATA ---
    total_vendors = Vendor.objects.count()
    total_customers = Customer.objects.count()
    now = timezone.now()
    upcoming_trips_count = Trip.objects.filter(trip_date__gte=now, status='Upcoming').count()
    completed_trips_count = Trip.objects.filter(status='Completed').count()

    # Calculate total agent revenue instead of total price
    total_agent_revenue_agg = Trip.objects.filter(status='Completed').aggregate(
        total=Sum(F('total_price') - F('vendor_price'), output_field=DecimalField())
    )
    total_agent_revenue = total_agent_revenue_agg['total'] or 0.00
    total_trips_count = Trip.objects.count()

    # --- LATEST TRIPS FOR TABLE ---
    latest_trips = Trip.objects.select_related('customer', 'vehicle').order_by('-created_at')[:5]

    # --- TRIPS ANALYTIC CHART DATA ---
    period = request.GET.get('period', 'week')
    chart_labels = []
    trip_series_data = []

    if period == 'month':
        start_date = now - timedelta(days=30)
        current_period_display = "Last 30 Days"
        period_trips = Trip.objects.filter(created_at__gte=start_date)
        trip_counts = period_trips.annotate(day=TruncDay('created_at')).values('day').annotate(
            count=Count('id')).order_by('day')
        data_map = {item['day'].strftime('%Y-%m-%d'): item['count'] for item in trip_counts}
        date_range = [(now - timedelta(days=i)) for i in range(29, -1, -1)]
        chart_labels = [date.strftime('%b %d') for date in date_range]
        trip_series_data = [data_map.get(date.strftime('%Y-%m-%d'), 0) for date in date_range]
    elif period == 'year':
        start_date = now - timedelta(days=365)
        current_period_display = "Last 12 Months"
        period_trips = Trip.objects.filter(created_at__gte=start_date)
        trip_counts = period_trips.annotate(month=TruncMonth('created_at')).values('month').annotate(
            count=Count('id')).order_by('month')
        data_map = {item['month'].strftime('%Y-%m'): item['count'] for item in trip_counts}
        month_range = [(now - timedelta(days=30 * i)) for i in range(11, -1, -1)]
        chart_labels = [date.strftime('%b %Y') for date in month_range]
        trip_series_data = [data_map.get(date.strftime('%Y-%m'), 0) for date in month_range]
    else:  # Default to 'week'
        start_date = now - timedelta(days=7)
        current_period_display = "Last 7 Days"
        period_trips = Trip.objects.filter(created_at__gte=start_date)
        trip_counts = period_trips.annotate(day=TruncDay('created_at')).values('day').annotate(
            count=Count('id')).order_by('day')
        data_map = {item['day'].strftime('%Y-%m-%d'): item['count'] for item in trip_counts}
        date_range = [(now - timedelta(days=i)) for i in range(6, -1, -1)]
        chart_labels = [date.strftime('%b %d') for date in date_range]
        trip_series_data = [data_map.get(date.strftime('%Y-%m-%d'), 0) for date in date_range]

    # Update period revenue calculation to use Agent Revenue
    period_revenue_agg = period_trips.filter(status='Completed').aggregate(
        total=Sum(F('total_price') - F('vendor_price'), output_field=DecimalField())
    )
    period_revenue = period_revenue_agg['total'] or 0.00

    sales_chart_options = {
        "series": [{"name": "Trips Created", "data": trip_series_data}],
        "chart": {"height": 350, "type": 'area', "toolbar": {"show": False}},
        "dataLabels": {"enabled": False},
        "stroke": {"curve": 'smooth', "width": 2},
        "xaxis": {"categories": chart_labels},
        "colors": ['#3e60d5'],
        "tooltip": {"x": {"format": 'dd MMM yyyy'}},
    }

    # --- TOP 5 VENDOR LIST DATA ---
    top_vendors = Vendor.objects.annotate(
        average_rating=Avg('ratings__stars'),
        num_ratings=Count('ratings')
    ).filter(average_rating__isnull=False).order_by('-average_rating', '-num_ratings')[:5]

    context = {
        "title": "Dashboard", "subtitle": "Analytics",
        "total_vendors": total_vendors, "total_customers": total_customers,
        "upcoming_trips_count": upcoming_trips_count,
        "total_revenue": f"{total_agent_revenue:,.2f}",  # This now represents agent revenue
        "latest_trips": latest_trips,
        "sales_chart_options": sales_chart_options,
        "current_period": period, "current_period_display": current_period_display,
        "period_revenue": f"{period_revenue:,.2f}",  # This now represents period agent revenue
        "top_vendors": top_vendors,
    }
    return render(request, 'dashboard.html', context)


def trip_feed_view(request):
    """
    Provides a daily summary of trips as a JSON feed for the FullCalendar.
    """
    daily_counts = Trip.objects.annotate(
        date=TruncDate('trip_date')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    events = []
    for daily_summary in daily_counts:
        events.append({
            'title': f"Total Trips: {daily_summary['count']}",
            'start': daily_summary['date'].isoformat(),
            'allDay': True,
        })

    return JsonResponse(events, safe=False)