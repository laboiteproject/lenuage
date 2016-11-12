# coding: UTF-8

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _L


class AppBikesConfig(AppConfig):
    name = 'laboite.apps.bikes'
    verbose_name = _L('App : vélos')
