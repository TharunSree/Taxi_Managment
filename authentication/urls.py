from django.urls import path
from . import views

urlpatterns = [
    path('create-staff/', views.create_staff_view, name='create_staff'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:pk>/update/', views.user_update_view, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete_view, name='user_delete'),
    path('users/<int:pk>/reset-password/', views.admin_reset_password_view, name='admin_reset_password'),
    path('profile/', views.profile_view, name='profile'),
    path('session-timed-out/', views.session_timed_out_view, name='session_timed_out'),
]
