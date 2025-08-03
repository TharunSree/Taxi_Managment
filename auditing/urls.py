from django.urls import path
from . import views

urlpatterns = [
    path('logs/', views.action_log_view, name='action_logs'),
]