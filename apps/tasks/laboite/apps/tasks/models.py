# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from datetime import timedelta

from boites.models import Boite, App
from . import settings

import asana

class AppTasks(App):
    asana_personal_access_token = models.CharField(_(u"Clé d'API Asana"), help_text=_(u"Veuillez indiquer votre clé d'API personnelle Asana (Personal Access Token)"), max_length=64, default=None, null=True)
    asana_project_id = models.PositiveIntegerField(_(u"Identifiant projet Asana"), help_text=_(u"Veuillez indiquer l'identifiant du projet Asana dans lequel vous souhaitez travailler"), default=None, null=True)

    # from https://asana.com/developers/api-reference/tasks
    name = models.CharField(_(u"Nom de la prochaine tâche"), max_length=128, default=None, null=True)
    tasks = models.PositiveSmallIntegerField(_(u"Nombre de tâches à traiter"), default=None, null=True)

    def get_app_dictionary(self):
        if self.enabled:
            # we wan't to update every VALUES_UPDATE_INTERVAL minutes
            if self.last_activity is None or timezone.now() >= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
                client = asana.Client.access_token(self.asana_personal_access_token)
                me = client.users.me()

                tasks = client.tasks.find_all({'project': self.asana_project_id, 'opt_fields' : 'due_on, completed, name, assignee'})
                uncompleted_tasks = 0
                self.name = None

                for task in tasks:
                    if task['completed'] is False and task['assignee'] is not None:
                        if task['assignee']['id'] == me['id']:
                            uncompleted_tasks += 1
                            if uncompleted_tasks == 1:
                                self.name = task['name']

                self.tasks = uncompleted_tasks
                self.save()

            return {'name': self.name, 'tasks' : self.tasks}

    class Meta:
        verbose_name = _("Configuration : tâches")
        verbose_name_plural = _("Configurations : tâches")
