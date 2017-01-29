# coding: utf-8
from boites.views import AppCreateView, AppUpdateView, AppDeleteView
from .models import AppWeather


class AppWeatherCreateView(AppCreateView):
    model = AppWeather
    fields = ['city_name']


class AppWeatherUpdateView(AppUpdateView):
    model = AppWeather
    fields = ['city_name', 'enabled']


class AppWeatherDeleteView(AppDeleteView):
    model = AppWeather
