from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppWifiConfig(AppConfig):
    name = label = 'laboite.apps.wifi'
    verbose_name = _('App : Wifi')
