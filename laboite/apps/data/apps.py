# coding: utf-8

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppDataConfig(AppConfig):
    name = label = 'laboite.apps.data'
    verbose_name = _('App : Données')
