from django.urls import path

from . import views

urlpatterns = [
    path('api', views.WeatherDataView.as_view(), name='api'),
]