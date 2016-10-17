# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.utils import timezone
from datetime import timedelta
import json
import requests

from boites.models import Boite, App
from app_metro_status import settings


def maybe_json(json_data):
    try:
        return json.loads(json_data)
    except ValueError:
        return


class AppMetroStatus(App):
    failures = models.TextField(_(u'Pannes'))

    def get_app_dictionary(self):
        if not self.enabled:
            return

        # we want to update every VALUES_UPDATE_INTERVAL minutes
        if timezone.now() <= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
            return maybe_json(self.failures)

        response = requests.get(settings.STAR_API_URL)
        if not response.status_code == 200:
            return maybe_json(self.failures)


        failures_data = response.json().get('records', [])

        # Get the fields for each returned record.
        failures = [failure.get('fields', {}) for failure in failures_data]
        failures = [{'line_name': failure.get('nomcourt'),
                     'end_failure': failure.get('finpanneprevue')}
                    for failure in failures
                    if failure.get('etat', 'OK') != 'OK']

        if not any(failures):
            return

        self.failures = json.dumps(failures)
        self.save()

        return failures

    class Meta:
        verbose_name = _("Configuration : statut lignes de métro")
        verbose_name_plural = _("Configurations : statut lignes de métro")
