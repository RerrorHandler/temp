from django.db import models
from django.utils import timezone

class TempData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    board_name = models.CharField(max_length=16)
    measure = models.CharField(max_length=16)
    data = models.CharField(max_length=16, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"{self.board_name} - {self.measure} - {self.data}"

class HumidityData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    board_name = models.CharField(max_length=16)
    measure = models.CharField(max_length=16)
    data = models.CharField(max_length=16)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.board_name} - {self.measure} - {self.data}"