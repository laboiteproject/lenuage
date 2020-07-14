# coding: utf-8
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppAirQualityConfig(AppConfig):
    name = label = 'laboite.apps.airquality'
    verbose_name = _("App : Qualité de l'air")
