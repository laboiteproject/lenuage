from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import timedelta

from boites.models import Boite, App
from app_tasks import settings

class AppTasks(App):
    asana_personal_access_token = models.CharField(_(u"Clé d'API Asana "), help_text=_(u"Veuillez indiquer votre clé d'API personnelle Asana (Personal Access Token)"), max_length=64, default=None, null=True)

    parcel_carrier = models.CharField(_(u"Transporteur"), help_text=_(u"Veuillez indiquer le transporteur de votre colis"), max_length=16, default="chronopost", choices=WEBOOB_MODULES_CHOICES)

    WEBOOB_PARCEL_STATUS_CHOICES = (
        (0, "Inconnu"),
        (1, "Traitement"),
        (2, "En transit"),
        (3, "Livré"),
    )
    status = models.PositiveSmallIntegerField(_(u"Statut"), choices=WEBOOB_PARCEL_STATUS_CHOICES, default=None, null=True)
    arrival = models.DateTimeField(_(u"Date de livraison"), null=True, default=None)
    url = models.URLField(_(u"Lien vers le site du transporteur"), default=None, null=True)

    def get_app_dictionary(self):
        if self.enabled:
            # we wan't to update every VALUES_UPDATE_INTERVAL minutes
            if self.status is None or timezone.now() >= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
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
                        self.save()

        return {'parcel': self.parcel, 'parcel_carrier' : self.parcel_carrier, 'status': self.status, 'arrival': self.arrival}

    class Meta:
        verbose_name = _("Configuration : colis")
        verbose_name_plural = _("Configurations : colis")
