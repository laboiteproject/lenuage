# coding: utf-8
from .models import AppWifi
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppWifiCreateView(AppCreateView):
    model = AppWifi
    fields = ['ssid', 'preshared_key']


class AppWifiUpdateView(AppUpdateView):
    model = AppWifi
    fields = ['ssid', 'preshared_key', 'enabled']


class AppWifiDeleteView(AppDeleteView):
    model = AppWifi
