# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.utils import formats, timezone
from django.utils.translation import ugettext_lazy as _
from icalendar import Calendar
import pytz
import requests

from boites.models import App


class AppCalendar(App):
    UPDATE_INTERVAL = 60 * 60

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

        calendar = calendar.from_ical(r.text.encode('ascii', 'replace'))

        for event in calendar.walk():
            if event.get('dtstart'):
                dtstart = event.get('dtstart').dt
                if not isinstance(dtstart, datetime):
                    dtstart = datetime.fromordinal(dtstart.toordinal())
                try:
                    dtstart = timezone.localtime(dtstart, timezone.utc)
                except ValueError:
                    dtstart = dtstart.replace(tzinfo=timezone.utc)
                if now <= dtstart <= tonight:
                    dtstart = timezone.localtime(dtstart, pytz.timezone('Europe/Paris'))
                    self.dtstart = formats.time_format(dtstart, 'TIME_FORMAT')
                    self.summary = str(event.get('summary'))
        self.save()

    def _get_data(self):
        return {'dtstart': self.dtstart,
                'summary': self.summary}

    class Meta:
        verbose_name = _('Configuration : calendrier')
        verbose_name_plural = _('Configurations : calendrier')
