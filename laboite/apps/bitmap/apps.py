# coding: utf-8
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppBitmapConfig(AppConfig):
    name = label = 'laboite.apps.bitmap'
    verbose_name = _('App : Icône personnalisée')
