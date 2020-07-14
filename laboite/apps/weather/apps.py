# coding: utf-8
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppWeatherConfig(AppConfig):
    name = label = 'laboite.apps.weather'
    verbose_name = _('App : Météo')
