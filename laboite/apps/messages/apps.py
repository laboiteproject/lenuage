from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppMessagesConfig(AppConfig):
    name = label = 'laboite.apps.messages'
    verbose_name = _('App : Message')
