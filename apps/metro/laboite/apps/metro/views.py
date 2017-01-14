# coding: utf-8

from boites.views import AppCreateView, AppUpdateView, AppDeleteView
from .models import AppMetro


class AppMetroCreateView(AppCreateView):
    model = AppMetro
    fields = ['enabled']


class AppMetroUpdateView(AppUpdateView):
    model = AppMetro
    fields = ['enabled']


class AppMetroDeleteView(AppDeleteView):
    model = AppMetro
