# coding: utf-8
from .models import AppLuftdaten
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppLuftdatenCreateView(AppCreateView):
    model = AppLuftdaten
    fields = ['sensor']


class AppLuftdatenUpdateView(AppUpdateView):
    model = AppLuftdaten
    fields = ['sensor', 'enabled']


class AppLuftdatenDeleteView(AppDeleteView):
    model = AppLuftdaten
