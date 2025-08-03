from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_list_view, name='vehicle_list'),
    path('add/', views.vehicle_add_view, name='vehicle_add'),
    path('<int:pk>/update/', views.vehicle_update_view, name='vehicle_update'),
    path('<int:pk>/delete/', views.vehicle_delete_view, name='vehicle_delete'),
    path('api/by-vendor/', views.vehicles_by_vendor_api, name='api_vehicles_by_vendor'),
]
