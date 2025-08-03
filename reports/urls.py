from django.urls import path
from . import views

urlpatterns = [
    path('trips/', views.trip_report_view, name='trip_report'),
    path('trips/<int:pk>/bill/', views.generate_bill_view, name='generate_bill'),
    path('trips/<int:pk>/pdf/customer/', views.generate_customer_pdf, name='pdf_customer_confirmation'),
    path('trips/<int:pk>/pdf/vendor/', views.generate_vendor_pdf, name='pdf_vendor_confirmation'),
]
