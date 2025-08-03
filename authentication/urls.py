from django.urls import path
from . import views

urlpatterns = [
    path('create-staff/', views.create_staff_view, name='create_staff'),
path('users/', views.user_list_view, name='user_list'),
    path('users/<int:pk>/update/', views.user_update_view, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete_view, name='user_delete'),
]