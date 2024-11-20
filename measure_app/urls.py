from django.urls import path
from . import views

urlpatterns = [
    path('receive_data/', views.receive_data, name='receive_data'),
    path('latest/', views.latest_measurements, name='latest_measurements'),
    path('latest-measurements-data/', views.latest_measurements_data, name='latest_measurements_data'),
]