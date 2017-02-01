# coding: utf-8
from __future__ import unicode_literals
from .models import AppTime
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppTimeCreateView(AppCreateView):
    model = AppTime
    fields = ['tz']


class AppTimeUpdateView(AppUpdateView):
    model = AppTime
    fields = ['tz', 'enabled']


class AppTimeDeleteView(AppDeleteView):
    model = AppTime
