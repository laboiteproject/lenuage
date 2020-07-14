from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppParkingConfig(AppConfig):
    name = label = 'laboite.apps.parking'
    verbose_name = _('App : parking')
