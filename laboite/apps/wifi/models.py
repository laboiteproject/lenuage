# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.models import App


class AppWifi(App):
    ssid = models.CharField(_('Nom du réseau'), help_text=_('Veuillez indiquer le nom de votre réseau wifi'), max_length=64)
    preshared_key  = models.CharField(_('Clé de protection'), help_text=_('Veuillez indiquer la clé de protection de votre réseau'), max_length=128)

    def _get_data(self):
        return {'ssid': self.ssid,
                'preshared_key': self.preshared_key}

    class Meta:
        verbose_name = _('Configuration : wifi')
        verbose_name_plural = _('Configurations : wifi')
