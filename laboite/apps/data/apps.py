# coding: utf-8
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppDataConfig(AppConfig):
    name = label = 'laboite.apps.data'
    verbose_name = _('App : Données')
