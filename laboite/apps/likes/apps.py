from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppLikesConfig(AppConfig):
    name = label = 'laboite.apps.likes'
    verbose_name = _('App : Facebook likes')
