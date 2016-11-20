# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from datetime import timedelta

from boites.models import Boite, App
from app_parcel import settings

from weboob.core import Weboob
from weboob.capabilities.parcel import CapParcel

class AppParcel(App):
    parcel = models.CharField(_(u"Identifiant du colis"), help_text=_(u"Veuillez saisir l'identifiant de votre colis"), max_length=64, default=_(u"XX123456789FR"), null=False, blank=False)

    WEBOOB_MODULES_CHOICES = (
        ("chronopost", _(u"Chronopost")),
        ("colisprive", _(u"Colisprive")),
        ("colissimo", _(u" Colissimo")),
        ("dhl", _(u"DHL")),
        ("dpd", _(u"DPD")),
        ("gls", _(u"GLS")),
        ("itella", _(u"Itella")),
        ("ups", _(u"UPS")),
    )
    parcel_carrier = models.CharField(_(u"Transporteur"), help_text=_(u"Veuillez indiquer le transporteur de votre colis"), max_length=16, default="chronopost", choices=WEBOOB_MODULES_CHOICES)

    WEBOOB_PARCEL_STATUS_CHOICES = (
        (0, "Inconnu"),
        (1, "Traitement"),
        (2, "En transit"),
        (3, "Livré"),
    )
    arrival = models.DateTimeField(_(u"Date de livraison"), null=True, default=None)
    status = models.PositiveSmallIntegerField(_(u"Statut"), choices=WEBOOB_PARCEL_STATUS_CHOICES, default=None, null=True)
    info = models.CharField(_(u"Informations"), max_length=64, null=True, blank=True)
    url = models.URLField(_(u"Lien vers le site du transporteur"), default=None, null=True)

    def get_app_dictionary(self):
        if self.enabled:
            # we wan't to update every VALUES_UPDATE_INTERVAL minutes
            if self.status != 3 or timezone.now() >= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
                # Weboob 1.2 example http://dev.weboob.org/
                weboob = Weboob()
                weboob.load_backends(CapParcel)
                for backend in list(weboob.iter_backends()):
                    if backend.name == self.parcel_carrier:
                        parcel = backend.get_parcel_tracking(self.parcel)
                        parcel_dict = parcel.to_dict()
                        self.status = parcel_dict['status']
                        if parcel_dict['arrival'] == 'Not loaded':
                            self.arrival = None
                        else:
                            pass
                            #parcel_dict['arrival']
                        self.url = parcel_dict['url']
                        self.info = parcel_dict['info']
                        self.save()

            return {'parcel': self.parcel, 'parcel_carrier' : self.parcel_carrier, 'arrival': self.arrival, 'status': self.status, 'info':self.info}

    class Meta:
        verbose_name = _("Configuration : colis")
        verbose_name_plural = _("Configurations : colis")
