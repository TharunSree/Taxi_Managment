from django.urls import path
from . import views

urlpatterns = [
    path('trips/', views.trip_report_view, name='trip_report'),
    path('trips/<int:pk>/bill/', views.generate_bill_view, name='generate_bill'),
]
