# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.models import App


class AppWifi(App):
    ssid = models.CharField(_('Nom du réseau'), max_length=64)
    preshared_key  = models.CharField(_('Clé de protection'), max_length=128)

    def _get_data(self):
        return {'ssid': self.ssid,
                'preshared_key': self.preshared_key}

    class Meta:
        verbose_name = _('Configuration : wifi')
        verbose_name_plural = _('Configurations : wifi')
