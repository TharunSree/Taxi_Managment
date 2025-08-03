"""
URL configuration for Taxi_Managment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib.auth import views as auth_views, logout

import authentication
from authentication.views import custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    # App URLs
    path('', include('dashboard.urls')),
    path('customers/', include('customers.urls')),
    path('vendors/', include('vendors.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('trips/', include('trips.urls')),
    path('auth/', include('authentication.urls')),
    path('calendar/', include('calendar_app.urls')),
    path('reports/', include('reports.urls')),
    path('config/', include('configuration.urls')),
    path('audit/', include('auditing.urls')),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', authentication.views.custom_logout, name='logout'),

]

