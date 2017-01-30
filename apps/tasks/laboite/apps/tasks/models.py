# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.models import App, MINUTES

import asana


class AppTasks(App):
    UPDATE_INTERVAL = 30 * MINUTES

    asana_personal_access_token = models.CharField(_("Clé d'API Asana"), help_text=_("Veuillez indiquer votre clé d'API personnelle Asana (Personal Access Token)"), max_length=64, default=None, null=True)
    asana_project_id = models.PositiveIntegerField(_('Identifiant projet Asana'), help_text=_("Veuillez indiquer l'identifiant du projet Asana dans lequel vous souhaitez travailler"), default=None, null=True)

    # from https://asana.com/developers/api-reference/tasks
    name = models.CharField(_('Nom de la prochaine tâche'), max_length=128, default=None, null=True)
    tasks = models.PositiveSmallIntegerField(_('Nombre de tâches à traiter'), default=None, null=True)

    def update_data(self):
        client = asana.Client.access_token(self.asana_personal_access_token)
        me = client.users.me()

        tasks = client.tasks.find_all({'project': self.asana_project_id,
                                       'opt_fields' : 'due_on, completed, name, assignee'})
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

    def _get_data(self):
        return {'name': self.name,
                'tasks': self.tasks}

    class Meta:
        verbose_name = _('Configuration : tâches')
        verbose_name_plural = _('Configurations : tâches')
