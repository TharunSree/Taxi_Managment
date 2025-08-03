from django.urls import path
from . import views


urlpatterns = [
    path('', views.trip_list_view, name='trip_list'),
    path('add/', views.trip_add_view, name='trip_add'),
    path('<int:pk>/update/', views.trip_update_view, name='trip_update'),
    path('<int:pk>/cancel/', views.trip_cancel_view, name='trip_cancel'),
    path('packages/', views.package_list_view, name='package_list'),
    path('packages/add/', views.package_add_view, name='package_add'),
    path('packages/<int:pk>/update/', views.package_update_view, name='package_update'),
    path('packages/<int:pk>/delete/', views.package_delete_view, name='package_delete'),
    path('<int:pk>/finalize/', views.trip_finalize_view, name='trip_finalize'),
    path('<int:pk>/rate/', views.add_rating_view, name='trip_rate'),
    path('api/trips-feed/', views.trip_feed_view, name='trip_feed'),
]


