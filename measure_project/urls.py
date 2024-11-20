"""
URL configuration for measure_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from measure_app.views import home, temperature_data_api, humidity_data_api, latest_measurements


urlpatterns = [
    path('admin/', admin.site.urls),
    path('measure/', include('measure_app.urls')),
    path('', home, name='home'),
    path('api/temperature-data/', temperature_data_api, name='temperature_data_api'),
    path('api/humidity-data/', humidity_data_api, name='humidity_data_api'),
    path('latest/', latest_measurements, name='latest_measurements'),


]
