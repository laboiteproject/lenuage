# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.models import App, MINUTES

import requests


class AppCoffees(App):
    UPDATE_INTERVAL = 5 * MINUTES

    url = models.URLField(_('URL du serveur laclef'), help_text=_("Veuillez indiquer l'adresse de votre serveur laclef"), default='http://demo.laclef.cc/', null=False)
    uid = models.CharField(_('Identifiant utilisateur'), help_text=_("Veuillez indiquer votre identifiant utilisateur"), max_length=32)
    daily = models.PositiveSmallIntegerField(_('Nombre de cafés consommés aujourd\'hui'), default=0)
    monthly = models.PositiveSmallIntegerField(_('Nombre de cafés consommés ce mois'), default=0)

    def _get_data(self):
        return {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'bitmap',
                    'width': 8,
                    'height': 8,
                    'x': 1,
                    'y': 0,
                    'color': 3,
					'font': 1,
					'content': '0x482448ff85868478',
                },
                {
                    'type': 'text',
                    'width': 10,
                    'height': 8,
                    'x': 11,
                    'y': 1,
                    'color': 2,
					'font': 1,
					'content':  '%s/%s' % (self.daily, self.monthly),
                },
            ]
        }

    def update_data(self):
        self.daily = 0
        self.monthly = 0

        url = self.url + "/coffees/" + self.uid
        r = requests.get(url)

        self.daily = int(r.json()['coffees']['today'])
        self.monthly = int(r.json()['coffees']['this_month'])
        self.save()

    class Meta:
        verbose_name = _('Configuration : cafés')
        verbose_name_plural = _('Configurations : cafés')
