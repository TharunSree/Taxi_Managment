from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_list_view, name='vendor_list'),
    path('add/', views.vendor_add_view, name='vendor_add'),
    path('<int:pk>/update/', views.vendor_update_view, name='vendor_update'),
    path('<int:pk>/delete/', views.vendor_delete_view, name='vendor_delete'),
    path('api/by-district/', views.vendors_by_district_api, name='api_vendors_by_district'),
]
