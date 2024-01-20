from django.db import models


class City(models.Model):
    """Model of city data"""
    name = models.CharField(max_length=100, help_text='City name')
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    last_requested_at = models.DateTimeField(null=True,
                                             blank=True,
                                             help_text='Last request time')
    last_temperature = models.DecimalField(max_digits=4,
                                           decimal_places=2,
                                           null=True,
                                           blank=True,
                                           help_text='Last temperature received from API')
    last_wind = models.DecimalField(max_digits=4,
                                           decimal_places=2,
                                           null=True,
                                           blank=True,
                                           help_text='Last wind data received from API')
    last_pressure = models.DecimalField(max_digits=5,
                                           decimal_places=2,
                                           null=True,
                                           blank=True,
                                           help_text='Last pressure data received from API')


    def __str__(self):
        return self.name
