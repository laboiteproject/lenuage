# coding: utf-8

from __future__ import unicode_literals

from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from boites.models import Boite, App
from . import providers, settings


class AppBikes(App):
    provider = models.CharField(_(u'Fournisseur de données'), help_text=_('Choisissez le service de vélos désiré'), choices=providers.get_providers(), max_length=64)
    station = models.TextField(_(u'Station'), help_text=_(u'Choisissez la station dont vous voulez obtenir les informations'))
    nb_stands = models.PositiveIntegerField(_(u'Nombre de places totales'), null=True)
    nb_available = models.PositiveIntegerField(_(u'Nombre de vélos disponibles'), null=True)
    status = models.NullBooleanField(_(u'En fonctionnement ?'), null=True)

    def get_provider_class(self):
        return providers.get_provider(self.provider)

    def get_app_dictionary(self):
        if self.enabled:
            if timezone.now() >= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
                cls = providers.get_provider(self.provider)
                data = cls.get_station_infos(self.station)
                for field in ('nb_stands', 'nb_available', 'status'):
                    setattr(self, field, data[field])
                self.save()
        return {
            'provider': self.provider,
            'station': self.station,
            'nb_stands': self.nb_stands,
            'nb_available': self.nb_available,
            'status': self.status
        }
