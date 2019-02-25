# coding: utf-8
from __future__ import unicode_literals
from .models import AppAirQuality
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppAirQualityCreateView(AppCreateView):
    model = AppAirQuality
    fields = []


class AppAirQualityUpdateView(AppUpdateView):
    model = AppAirQuality
    fields = ['enabled']


class AppAirQualityDeleteView(AppDeleteView):
    model = AppAirQuality
