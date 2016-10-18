# coding: UTF-8

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext as _


class AppBikesConfig(AppConfig):
    name = 'app_bikes'
    verbose_name = _(u'App : vélos')
