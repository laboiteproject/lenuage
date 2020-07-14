# coding: utf-8
from .models import AppData
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppDataCreateView(AppCreateView):
    model = AppData
    fields = ['url', 'prepend', 'append']


class AppDataUpdateView(AppUpdateView):
    model = AppData
    fields = ['url', 'prepend', 'append', 'json_path', 'enabled']


class AppDataDeleteView(AppDeleteView):
    model = AppData
