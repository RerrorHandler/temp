from django.contrib import admin
from .models import TempData, HumidityData

admin.site.register(TempData)
admin.site.register(HumidityData)