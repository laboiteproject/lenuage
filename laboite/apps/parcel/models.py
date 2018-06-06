# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.models import MINUTES, App

from weboob.core import Weboob
from weboob.capabilities.base import NotLoaded


WEBOOB_MODULES_CHOICES = (
    ('chronopost', _('Chronopost')),
    ('colisprive', _('Colis privé')),
    ('colissimo', _('Colissimo')),
    ('dpd', _('DPD')),
    ('dhl', _('DHL')),
    ('gls', _('GLS')),
    ('itella', _('Itella')),
    ('ups', _('UPS')),
)


WEBOOB_PARCEL_STATUS_CHOICES = (
    (0, _('Inconnu')),
    (1, _('Traitement')),
    (2, _('En transit')),
    (3, _('Livré')),
)


class AppParcel(App):
    UPDATE_INTERVAL = 10 * MINUTES

    parcel = models.CharField(_('Identifiant du colis'), help_text=_("Veuillez saisir l'identifiant de votre colis"), max_length=64, default=_('XX123456789FR'), null=False, blank=False)
    parcel_carrier = models.CharField(_('Transporteur'), help_text=_('Veuillez indiquer le transporteur de votre colis'), max_length=16, default='chronopost', choices=WEBOOB_MODULES_CHOICES)
    arrival = models.DateTimeField(_('Date de livraison'), null=True, default=None)
    status = models.PositiveSmallIntegerField(_('Statut'), choices=WEBOOB_PARCEL_STATUS_CHOICES, default=None, null=True)
    info = models.CharField(_('Informations'), max_length=64, null=True, blank=True)
    url = models.URLField(_('Lien vers le site du transporteur'), default=None, null=True)

    def update_data(self):
        weboob = Weboob()
        backend = weboob.load_backend(self.parcel_carrier, None)
        parcel = backend.get_parcel_tracking(self.parcel)
        parcel_dict = parcel.to_dict()
        self.status = parcel_dict['status']
        self.arrival = parcel_dict['arrival'] if parcel_dict['arrival'] is not NotLoaded else None
        self.url = parcel_dict['url'] if parcel_dict['url'] is not NotLoaded else None
        self.info = parcel_dict['info']
        self.save()

    def _get_data(self):
        parcel_status = 'OK' if self.status == 3 else 'In transit'
        return {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'bitmap',
                    'width': 12,
                    'height': 8,
                    'x': 0,
                    'y': 0,
                    'color': 2,
					'content': '0xfe0ff8fe4fe2ffe802a0adf6208'
                },
                {
                    'type': 'text',
                    'width': len(str(parcel_status)) * 5+1,
                    'height': 8,
                    'x': 12,
                    'y': 2,
                    'color': 2,
					'font': 1,
					'content': "%s" % parcel_status,
                },
            ]
        }


        return {'parcel': self.parcel,
                'parcel_carrier': self.parcel_carrier,
                'arrival': self.arrival,
                'status': self.status,
                'info': self.info}

    class Meta:
        verbose_name = _('Configuration : colis')
        verbose_name_plural = _('Configurations : colis')
