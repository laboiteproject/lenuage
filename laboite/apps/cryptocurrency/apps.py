from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppCryptocurrencyConfig(AppConfig):
    name = label = 'laboite.apps.cryptocurrency'
    verbose_name = _('App : Crypto-monnaie')
