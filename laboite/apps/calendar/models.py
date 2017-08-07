# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.utils import formats, timezone
from django.utils.translation import ugettext_lazy as _
from icalendar import Calendar
import pytz
import requests
import unidecode

from boites.models import App, HOURS


class AppCalendar(App):
    UPDATE_INTERVAL = 1 * HOURS

    ics_url = models.CharField(_('URL du calendrier .ics'), help_text=_("Veuillez indiquer l'adresse de votre calendrier .ics"), max_length=256, default=None, null=True)
    dtstart = models.CharField(_('Heure du prochain rendez-vous'), max_length=5, default=None, null=True)
    summary = models.CharField(_('Intitulé du prochain rendez-vous'), max_length=256, default=None, null=True)

    def update_data(self):
        # TODO: handle whole day events, display multiple events
        now = timezone.now()
        tonight = now.replace(hour=23, minute=59)

        self.dtstart = None
        self.summary = None

        calendar = Calendar()
        r = requests.get(self.ics_url)

        calendar = calendar.from_ical(unidecode.unidecode(r.text))

        for event in calendar.walk():
            if event.get('dtstart') and event.get('dtend'):
                dtstart = event.get('dtstart').dt
                dtend = event.get('dtend').dt
                if not isinstance(dtstart, datetime) or not isinstance(dtend, datetime):
                    dtstart = datetime.fromordinal(dtstart.toordinal())
                    dtend = datetime.fromordinal(dtend.toordinal())
                try:
                    dtstart = timezone.localtime(dtstart, timezone.utc)
                    dtend = timezone.localtime(dtend, timezone.utc)
                except ValueError:
                    dtstart = dtstart.replace(tzinfo=timezone.utc)
                    dtend = dtend.replace(tzinfo=timezone.utc)
                if now <= dtend <= tonight:
                    dtstart = timezone.localtime(dtstart, pytz.timezone('Europe/Paris'))
                    self.dtstart = formats.time_format(dtstart, 'TIME_FORMAT')
                    self.summary = str(event.get('summary'))
        self.save()

    def _get_data(self):
        if self.dtstart:
            return {
                'width': 32,
                'height': 16,
                'update-interval': self.UPDATE_INTERVAL,
                'icon-calendar': {
                    'type': 'icon',
                    'width': 8,
                    'height': 8,
                    'x': 1,
                    'y': 0,
                    'content':
                        [
                            1,1,1,1,1,1,1,0,
                            1,1,1,1,1,1,1,0,
                            1,0,0,0,0,0,1,0,
                            1,0,0,1,0,0,1,0,
                            1,0,0,1,0,0,1,0,
                            1,0,0,1,0,0,1,0,
                            1,0,0,0,0,0,1,0,
                            1,1,1,1,1,1,1,0,
                        ]
                },
                'text-hours': {
                    'type': 'text',
                    'width': 10,
                    'height': 8,
                    'x': 9,
                    'y': 1,
                    'content': self.dtstart[:2],
                },
                'text-colon': {
                    'type': 'text',
                    'width': 24,
                    'height': 8,
                    'x': 18,
                    'y': 1,
                    'content': ':',
                },
                'text-minutes': {
                    'type': 'text',
                    'width': 24,
                    'height': 8,
                    'x': 22,
                    'y': 1,
                    'content': self.dtstart[-2:],
                },
                'text-summary': {
                    'type': 'text',
                    'width': 32,
                    'height': 8,
                    'scrolling': True,
                    'x': 0,
                    'y': 9,
                    'content': self.summary,
                }
            }
        else:
            return {
                'width': 32,
                'height': 8,
                'update-interval': self.UPDATE_INTERVAL,
                'text-meetings': {
                    'type': 'text',
                    'width': 10,
                    'height': 8,
                    'x': 0,
                    'y': 1,
                    'content': '0',
                },
                'icon-calendar': {
                    'type': 'icon',
                    'width': 8,
                    'height': 8,
                    'x': 6,
                    'y': 0,
                    'content':
                        [
                            1,1,1,1,1,1,1,0,
                            1,1,1,1,1,1,1,0,
                            1,0,0,0,0,0,1,0,
                            1,0,0,1,0,0,1,0,
                            1,0,0,1,0,0,1,0,
                            1,0,0,1,0,0,1,0,
                            1,0,0,0,0,0,1,0,
                            1,1,1,1,1,1,1,0,
                        ]
                },
            }

    class Meta:
        verbose_name = _('Configuration : calendrier')
        verbose_name_plural = _('Configurations : calendrier')
