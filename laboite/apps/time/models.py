# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.utils import formats, timezone
from django.db import models

import pytz

from boites.models import App, MINUTES

TZ_CHOICES = [(tz, _(tz)) for tz in pytz.common_timezones]


class AppTime(App):
    UPDATE_INTERVAL = 1 * MINUTES

    time = models.CharField(_('Heure'), max_length=32, null=True, default=None)
    date = models.CharField(_('Date'), max_length=32, null=True, default=None)
    tz = models.CharField(_('Fuseau horaire'),
                          help_text=_('Veuillez saisir un fuseau horaire pour votre boîte'),
                          max_length=32, default=_('Europe/Paris'), choices=TZ_CHOICES)

    @property
    def timezone(self):
        return pytz.timezone(self.tz)

    def update_data(self):
        now = timezone.localtime(timezone.now(), self.timezone)

        self.time = formats.time_format(now, 'TIME_FORMAT')
        self.date = formats.date_format(now, 'SHORT_DATE_FORMAT')
        self.save()

    def _get_data(self):
        return {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'text',
                    'width': 25,
                    'height': 8,
                    'x': 4,
                    'y': 1,
                    'color': 2,
                    'font': 1,
                    'content': self.time,
                },
            ]
        }

    class Meta:
        verbose_name = _('Configuration : temps')
        verbose_name_plural = _('Configurations : temps')
