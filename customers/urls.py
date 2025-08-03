from django.urls import path
from . import views

urlpatterns = [
    # This will be the page that lists all customers
    path('', views.customer_list_view, name='customer_list'),

    # We will create the views for these URLs in the next steps
    path('add/', views.customer_add_view, name='customer_add'),
    path('<int:pk>/update/', views.customer_update_view, name='customer_update'),
    path('<int:pk>/delete/', views.customer_delete_view, name='customer_delete'),
    path('add/ajax/', views.customer_add_ajax_view, name='customer_add_ajax'),
]
