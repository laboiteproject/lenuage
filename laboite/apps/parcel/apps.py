from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppParcelConfig(AppConfig):
    name = label = 'laboite.apps.parcel'
    verbose_name = _('App : Colis')
