# coding: utf-8
from .models import AppEnergy
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppEnergyCreateView(AppCreateView):
    model = AppEnergy
    fields = ['url', 'power_feedid', 'kwhd_feedid', 'emoncms_read_apikey']


class AppEnergyUpdateView(AppUpdateView):
    model = AppEnergy
    fields = ['url', 'power_feedid', 'kwhd_feedid', 'emoncms_read_apikey', 'enabled']


class AppEnergyDeleteView(AppDeleteView):
    model = AppEnergy
