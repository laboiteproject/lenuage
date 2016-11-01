# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from boites.models import Boite, App
from . import settings

from icalendar import Calendar, Event
from datetime import datetime, timedelta
import requests
from account.conf import settings
import pytz

from . import settings

class AppCalendar(App):
    ics_url = models.CharField(_(u"URL du calendrier ics"), help_text=_(u"Veuillez indiquer l'adresse de votre calendrier .ics"), max_length=256, default=None, null=True)

    dtstart = models.CharField(_(u"Heure du prochain rendez-vous"), max_length=5, default=None, null=True)
    summary = models.CharField(_(u"Intitulé du prochain rendez-vous"), max_length=256, default=None, null=True)

    def get_app_dictionary(self):
        if self.enabled:
            # we wan't to update every VALUES_UPDATE_INTERVAL minutes
            if self.dtstart is None or timezone.now() >= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
                now = timezone.now()
                today = now.replace(hour = 0, minute=0)
                tonight = now.replace(hour = 23, minute=59)

                self.dtstart = None
                self.summary = None
                self.save()

                calendar = Calendar()
                r = requests.get(self.ics_url)

                calendar = calendar.from_ical(r.text.encode('ascii', 'replace'))

                for event in calendar.walk():
                    # the following code is just bad
                    #TODO need improvements
                    if event.get('dtstart'):
                        dtstart = event.get('dtstart').dt
                        if type(dtstart) is not type(now):
                            # crapy conversion
                            dtstart = datetime.fromordinal(dtstart.toordinal())
                        dtstart = dtstart.replace(tzinfo = pytz.timezone('UTC'))
                        if dtstart > today and dtstart > now and dtstart < tonight:
                            self.dtstart = dtstart.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%H:%M")
                            self.summary = str(event.get('summary'))
                            self.save()

        return {'dtstart': self.dtstart, 'summary' : self.summary}

    class Meta:
        verbose_name = _("Configuration : calendrier")
        verbose_name_plural = _("Configurations : calendrier")
