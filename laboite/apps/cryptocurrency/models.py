# coding: utf-8

from __future__ import unicode_literals

import requests
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from boites.models import App, MINUTES


class AppCryptocurrency(App):
    UPDATE_INTERVAL = 10 * MINUTES

    CRYPTOCURRENCY_CHOICES = (
        ('bitcoin', _('Bitcoin')),
        ('ethereum', _('Ethereum')),
        ('bitcoin-cash', _('Bitcoin Cash')),
        ('ripple', _('Ripple')),
        ('dash', _('Dash')),
    )
    CURRENCY_CHOICES = (
        ('USD', _('Dollars')),
        ('EUR', _('Euros')),
    )
    cryptocurrency = models.CharField(_('Crypto-monnaie'), help_text=_('Veuillez indiquer la crypto-monnaie que vous souhaitez convertir'), max_length=16, default='bitcoin', choices=CRYPTOCURRENCY_CHOICES)
    currency = models.CharField(_('Monnaie'), help_text=_('Veuillez indiquer la devise dans laquelle vous souhaitez convertir'), max_length=8, default='EUR', choices=CURRENCY_CHOICES)
    value = models.PositiveSmallIntegerField(_('Valeur'), default=0)

    def _get_data(self):
        width = len(str(self.value)) * 5

        # $ symbol
        bitmap = '0x0040e08060e040'
        if self.currency == 'EUR':
            # € symbol
            bitmap = '0x003040e0e04030'
        return {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'text',
                    'width': width,
                    'height': 8,
                    'x': 0,
                    'y': 1,
                    'color': 2,
					'font': 1,
					'content':  '%s' % self.value,
                },
                {
                    'type': 'bitmap',
                    'width': 8,
                    'height': 8,
                    'x': width,
                    'y': 0,
                    'color': 2,
					'content': bitmap,
                },
            ]
        }

    def update_data(self):
        params = {'convert': self.currency,
                  'limit': 10}
        r = requests.get(settings.COINMARKETCAP_BASE_URL, params=params)

        for i in r.json():
            if i.get('id') == self.cryptocurrency:
                if self.currency == 'EUR':
                    self.value = float(i.get('price_eur'))
                else:
                    self.value = float(i.get('price_usd'))

        self.save()

    class Meta:
        verbose_name = _('Configuration : crypto-monnaie')
        verbose_name_plural = _('Configurations : crypto-monnaie')
