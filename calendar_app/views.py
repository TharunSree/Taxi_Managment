import calendar
from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate  # Corrected from TruncDay
from django.db.models import Count
from trips.models import Trip


@login_required
def calendar_view(request):
    try:
        year = int(request.GET.get('year', date.today().year))
        month = int(request.GET.get('month', date.today().month))
    except ValueError:
        today = date.today()
        year = today.year
        month = today.month

    # Get all trips for the given month and year
    trips_in_month = Trip.objects.filter(trip_date__year=year, trip_date__month=month).select_related('customer',
                                                                                                      'vehicle',
                                                                                                      'vehicle__vendor')

    # Group by date and get the count with trip details
    daily_trip_counts = (
        trips_in_month.annotate(date_only=TruncDate('trip_date'))
        .values('date_only')
        .annotate(count=Count('id'))
        .values('date_only', 'count')
    )

    # Convert to dictionary {day: count}
    trip_counts = {item['date_only'].day: item['count'] for item in daily_trip_counts}

    # Get trip details for tooltips
    trip_details = {}
    for trip in trips_in_month:
        day = trip.trip_date.day
        if day not in trip_details:
            trip_details[day] = []
        trip_details[day].append({
            'customer': trip.customer.name,
            'vehicle': str(trip.vehicle),
            'vendor': trip.vehicle.vendor.name,
            'status': trip.get_status_display(),
            'id': trip.id
        })

    # Generate calendar grid
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)

    # Calculate navigation dates
    if month == 1:
        prev_month = {'year': year - 1, 'month': 12}
    else:
        prev_month = {'year': year, 'month': month - 1}

    if month == 12:
        next_month = {'year': year + 1, 'month': 1}
    else:
        next_month = {'year': year, 'month': month + 1}

    # Calculate statistics
    total_trips = sum(trip_counts.values())
    active_days = len(trip_counts)
    avg_daily = round(total_trips / active_days, 1) if active_days > 0 else 0
    busiest_day = max(trip_counts.values()) if trip_counts else 0

    context = {
        'title': 'Trip Calendar',
        'month_days': month_days,
        'month_name': calendar.month_name[month],
        'current_year': year,
        'current_month': month,
        'trip_counts': trip_counts,
        'trip_details': trip_details,
        'prev_month': prev_month,
        'next_month': next_month,
        'today': date.today(),
        'total_trips': total_trips,
        'active_days': active_days,
        'avg_daily': avg_daily,
        'busiest_day': busiest_day,
    }
    return render(request, 'calendar/calendar.html', context)

