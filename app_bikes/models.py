# coding: utf-8

from __future__ import unicode_literals

from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from boites.models import Boite, App
from . import providers, settings


class AppBikes(App):
    provider = models.CharField(_('Fournisseur de données'), help_text=_('Choisissez le service de vélos désiré'), choices=providers.get_providers(), max_length=64)
    id_station = models.CharField(_('Identifiant station'), help_text=_('Choisissez la station dont vous voulez obtenir les informations'), max_length=64)
    station = models.TextField(_('Nom station'))
    slots = models.PositiveIntegerField(_('Nombre de places totales'), null=True)
    bikes = models.PositiveIntegerField(_('Nombre de vélos disponibles'), null=True)
    status = models.NullBooleanField(_('En fonctionnement ?'), null=True)

    def get_provider_class(self):
        return providers.get_provider(self.provider)

    def get_app_dictionary(self):
        if self.enabled:
            if timezone.now() >= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
                cls = providers.get_provider(self.provider)
                data = cls.get_station_infos(self.id_station)
                for field in ('station', 'slots', 'bikes', 'status'):
                    setattr(self, field, data[field])
                self.save()
        return {
            'provider': self.provider,
            'station': self.station,
            'slots': self.slots,
            'bikes': self.bikes,
            'status': self.status
        }

    class Meta:
        verbose_name = _('Configuration : vélos')
        verbose_name_plural = _('Configurations : vélos')
