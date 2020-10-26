# coding: utf-8
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppLuftdatenConfig(AppConfig):
    name = label = 'laboite.apps.luftdaten'
    verbose_name = _("App : Sensor.Community")
