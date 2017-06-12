from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppTimeConfig(AppConfig):
    name = label = 'laboite.apps.time'
    verbose_name = _('App : Temps')
