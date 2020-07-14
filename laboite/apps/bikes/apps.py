# coding: UTF-8
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppBikesConfig(AppConfig):
    name = label = 'laboite.apps.bikes'
    verbose_name = _('App : vélos')
