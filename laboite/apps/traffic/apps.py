from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppTrafficConfig(AppConfig):
    name = label = 'laboite.apps.traffic'
    verbose_name = _('App : Trafic')
