# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.utils import timezone
from datetime import timedelta
from django.db import models

from boites.models import App, MINUTES

import requests


class AppEnergy(App):
    UPDATE_INTERVAL = 30 * MINUTES

    url = models.URLField(_('URL du serveur emoncms'), help_text=_("Veuillez indiquer l'adresse de votre serveur emoncms"), default='https://emoncms.org/', null=False)
    power_feedid = models.PositiveSmallIntegerField(_('Identifiant flux puissance instantanée'), help_text=_('Veuillez saisir le numéro du flux lié à votre consommation instantannée (en watts)'), default=None, null=True)
    kwhd_feedid = models.PositiveSmallIntegerField(_('Identifiant flux consommation cumulée'), help_text=_('Veuillez saisir le numéro du flux lié à votre consommation cumulée (en kWh/j)'), default=None, null=True)
    emoncms_read_apikey = models.CharField(_("Clé d'API emoncms"), help_text=_("Veuillez indiquer votre clé d'API emoncms (lecture seule)"), max_length=32, default=None, null=True)
    power = models.PositiveSmallIntegerField(_('Consommation instantanée'), default=None, null=True)
    day0 = models.PositiveSmallIntegerField(_('Consommation j-6 (en kWh)'), default=None, null=True)
    day1 = models.PositiveSmallIntegerField(_('Consommation j-5 (en kWh)'), default=None, null=True)
    day2 = models.PositiveSmallIntegerField(_('Consommation j-4 (en kWh)'), default=None, null=True)
    day3 = models.PositiveSmallIntegerField(_('Consommation j-3 (en kWh)'), default=None, null=True)
    day4 = models.PositiveSmallIntegerField(_('Consommation j-2 (en kWh)'), default=None, null=True)
    day5 = models.PositiveSmallIntegerField(_('Consommation hier (en kWh)'), default=None, null=True)
    day6 = models.PositiveSmallIntegerField(_("Consommation aujourd'hui (en kWh)"), default=None, null=True)

    def update_data(self):
        self.power = None
        for i in range(7):
            setattr(self, 'day{}'.format(i), None)

        now = timezone.now()

        url = self.url.rstrip('/') + '/feed/timevalue.json'
        params = {'id': str(self.power_feedid),
                  'apikey': self.emoncms_read_apikey}
        r = requests.get(url, params=params)

        self.power = int(float(r.json().get('value')))

        last_week = now - timedelta(days=7)

        url = self.url.rstrip('/') + '/feed/data.json'
        params = {'id': str(self.kwhd_feedid),
                  'start': str(int(last_week.strftime('%s')) * 1000),
                  'end': str(int(now.strftime('%s')) * 1000),
                  'interval': 86400,
                  'skipmissing': 0,
                  'limitinterval': 1,
                  'apikey': self.emoncms_read_apikey}
        r = requests.get(url, params=params)
        values = [v[1] for v in r.json()[:7]]
        try:
            self.day0, self.day1, self.day2, self.day3, self.day4, self.day5, self.day6 = values
        except IndexError:
            pass

        self.save()

    def _get_data(self):
        return {'power': self.power,
                'day0': self.day0,
                'day1': self.day1,
                'day2': self.day2,
                'day3': self.day3,
                'day4': self.day4,
                'day5': self.day5,
                'day6': self.day6}

    class Meta:
        verbose_name = _("Configuration : énergie")
        verbose_name_plural = _("Configurations : énergie")
