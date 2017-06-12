# coding: utf-8
from __future__ import unicode_literals
from .models import AppAlarm
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppAlarmCreateView(AppCreateView):
    model = AppAlarm
    fields = ['heure', 'minutes']


class AppAlarmUpdateView(AppUpdateView):
    model = AppAlarm
    fields = ['heure', 'minutes', 'enabled']


class AppAlarmDeleteView(AppDeleteView):
    model = AppAlarm
