# coding: utf-8

from __future__ import unicode_literals

import requests
from django.db import models
from django.utils.translation import ugettext_lazy as _

from boites.models import App, MINUTES
from . import settings


class AppParking(App):
    UPDATE_INTERVAL = 5 * MINUTES
    API_BASE_URL = 'https://data.explore.star.fr/api/records/1.0/search'

    CAR_PARK_CHOICES = (
        ('HFR', "Henri Fréville"),
        ('JFK', "J.F. Kennedy"),
        ('POT', "La Poterie"),
        ('PRE', "Les Préales"),
        ('VU', "Villejean-Université"),
    )
    parking = models.CharField(
        help_text=_("Veuillez sélectionner votre parking"),
        max_length=3,
        choices=CAR_PARK_CHOICES,
    )

    open = models.NullBooleanField(_('Parking ouvert ?'), default=None, null=True)
    available = models.PositiveSmallIntegerField(_('Places disponibles'), default=None, null=True)
    occupied = models.PositiveSmallIntegerField(_('Places occupées'), default=None, null=True)

    def should_update(self):
        return super(AppParking, self).should_update() or self.open is None

    def update_data(self):
        params = {
            'dataset': 'tco-parcsrelais-etat-tr',
            'rows': 1,
            'apikey': settings.STAR_API_KEY,
            'q': 'idparc={}'.format(self.parking)
        }

        self.open = None
        self.available = None
        self.occupied = None

        r = requests.get(self.API_BASE_URL, params=params)

        records = r.json().get('records')
        if records:
            if records[0]['fields']['etat'] != "Fermé":
                self.open = True
                self.available = records[0]['fields']['nombreplacesdisponibles']
                self.occupied = records[0]['fields']['nombreplacesoccupees']
            else:
                self.open = False

        self.save()

    def _get_data(self):
        return {'parking': self.parking,
                'open': self.open,
                'available': self.available,
                'occupied': self.occupied}

    class Meta:
        verbose_name = _('Configuration : Parking')
        verbose_name_plural = _('Configurations : Parking')
