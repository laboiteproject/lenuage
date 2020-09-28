from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppCalendarConfig(AppConfig):
    name = label = 'laboite.apps.calendar'
    verbose_name = _('App : calendrier')
