# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.models import App


class AppCustom(App):
    icon = models.CharField(_('Nom du réseau'), max_length=64)
    message = models.TextField(_('Message personnalisé'), help_text=_('Veuillez indiquer le message pour cette app'), max_length=140, default='', blank=True)

    def _get_data(self):
        return {'icon': self.icon,
                'message': self.message}

    class Meta:
        verbose_name = _('Configuration : App personnalisée')
        verbose_name_plural = _('Configurations : App personnalisée')
