# coding: utf-8

from __future__ import unicode_literals

import decimal

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
    cryptocurrency = models.CharField(_('Crypto-monnaie'),
                                      help_text=_('Veuillez indiquer la crypto-monnaie que vous souhaitez convertir'),
                                      max_length=16, default='bitcoin', choices=CRYPTOCURRENCY_CHOICES)
    currency = models.CharField(_('Monnaie'),
                                help_text=_('Veuillez indiquer la devise dans laquelle vous souhaitez convertir'),
                                max_length=8, default='EUR', choices=CURRENCY_CHOICES)
    value = models.DecimalField(_('Valeur'), max_digits=8, decimal_places=3, default=0)

    def _get_data(self):
        #  Convert as str and keep only 5 chars max (without decimal separator)
        value = str(self.value)[:5].rstrip('.')
        width = len(value) * 5

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
                    'content': value,
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
                  'structure': 'array',
                  'limit': 20}
        r = requests.get(settings.COINMARKETCAP_BASE_URL, params=params)

        # FIXME: this means the wanted crypto has to be in the 20 results,
        # if it is not anymore, we'll never get its value
        for data in r.json()['data']:
            if data['website_slug'] == self.cryptocurrency:
                self.value = decimal.Decimal(data['quotes'][self.currency]['price'])
                break
        else:
            # Crypto not found
            self.value = 0
        self.save()

    class Meta:
        verbose_name = _('Configuration : crypto-monnaie')
        verbose_name_plural = _('Configurations : crypto-monnaie')
