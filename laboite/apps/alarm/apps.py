from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppAlarmConfig(AppConfig):
    name = label = 'laboite.apps.alarm'
    verbose_name = _('App : Alarmes')
