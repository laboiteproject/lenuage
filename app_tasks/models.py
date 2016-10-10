# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.utils import timezone
from datetime import timedelta

from boites.models import Boite, App
from app_tasks import settings

class AppTasks(App):
    asana_personal_access_token = models.CharField(_(u"Clé d'API Asana "), help_text=_(u"Veuillez indiquer votre clé d'API personnelle Asana (Personal Access Token)"), max_length=64, default=None, null=True)

    # from https://asana.com/developers/api-reference/tasks
    name = models.CharField(_(u"Nom de la prochaine tâche"), max_length=128, default=None, null=True)
    tasks = models.PositiveSmallIntegerField(_(u"Nombre de tâches à traiter"), default=None, null=True)

    def get_app_dictionary(self):
        if self.enabled:
            # we wan't to update every VALUES_UPDATE_INTERVAL minutes
            if self.name is None or timezone.now() >= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
                # bullshit value since I got a Connection reset by peer today
                #client = asana.Client.access_token("0/32bf71e2de8bb225be896e7a13111fbe")
                #workspaces = client.workspaces.find_all()

                self.name = "vérifier les div de la page Le MOOC en un coup d'oeil"
                self.tasks = 4
                self.save()

        return {'name': self.name, 'tasks' : self.tasks}

    class Meta:
        verbose_name = _("Configuration : tâches")
        verbose_name_plural = _("Configurations : tâches")
