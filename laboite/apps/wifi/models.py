# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.models import App


class AppWifi(App):
    ssid = models.CharField(_('Nom du réseau'), help_text=_('Veuillez indiquer le nom de votre réseau wifi'), max_length=64)
    preshared_key  = models.CharField(_('Clé de protection'), help_text=_('Veuillez indiquer la clé de protection de votre réseau'), max_length=128)

    def _get_data(self):
        return {
            'width': 32,
            'height': 16,
            'data':[
                {
                    'type': 'bitmap',
                    'width': 8,
                    'height': 6,
                    'x': 2,
                    'y': 0,
                    'color': 2,
					'font': 1,
					'content': '0x384492280010'
                },
                {
                    'type': 'text',
                    'width': 10,
                    'height': 8,
                    'x': 10,
                    'y': 1,
                    'color': 2,
					'font': 1,
					'content': "wifi",
                },
                {
                    'type': 'text',
                    'width': 32,
                    'height': 8,
                    'x': 0,
                    'y': 9,
                    'color': 2,
					'font': 1,
					'content': self.ssid + '/' + self.preshared_key,
                }
            ]
        }
    class Meta:
        verbose_name = _('Configuration : wifi')
        verbose_name_plural = _('Configurations : wifi')
