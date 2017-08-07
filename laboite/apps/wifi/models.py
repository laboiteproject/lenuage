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
            'update-interval': self.UPDATE_INTERVAL,
            'icon-wifi': {
                'type': 'icon',
                'width': 7,
                'height': 6,
                'x': 2,
                'y': 0,
                'content':
                    [
                        0,0,1,1,1,0,0,
                        0,1,0,0,0,1,0,
                        1,0,0,1,0,0,1,
                        0,0,1,0,1,0,0,
                        0,0,0,0,0,0,0,
                        0,0,0,1,0,0,0,
                    ]
            },
            'text-wifi': {
                'type': 'text',
                'width': 10,
                'height': 8,
                'x': 10,
                'y': 1,
                'content': "wifi",
            },
            'text-ssid': {
                'type': 'text',
                'width': 32,
                'height': 8,
                'scrolling': True,
                'x': 0,
                'y': 9,
                'content': self.ssid + '/' + self.preshared_key,
            }
        }
    class Meta:
        verbose_name = _('Configuration : wifi')
        verbose_name_plural = _('Configurations : wifi')
