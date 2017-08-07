# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.models import App, MINUTES

import asana


def get_projects(asana_personal_access_token):
    client = asana.Client.access_token(asana_personal_access_token)
    workspaces = client.workspaces.find_all()
    results = []
    for workspace in workspaces:
        projects = client.projects.find_all({'workspace': workspace['id']})
        for project in projects:
            results.append({'id': project['id'], 'name': project['name']})
    results.sort(key=lambda proj: proj['name'])
    return results


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
                                       'opt_fields': 'due_on, completed, name, assignee'})
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
        return {
            'width': 32,
            'height': 16,
            'update-interval': self.UPDATE_INTERVAL,
            'icon-tasks': {
                'type': 'icon',
                'width': 8,
                'height': 8,
                'x': 8,
                'y': 0,
                'content':
                    [
                        1,1,1,1,1,1,1,1,
                        1,1,1,1,1,1,1,1,
                        1,1,1,1,1,1,0,1,
                        1,0,1,1,1,0,0,1,
                        1,0,0,1,0,0,1,1,
                        1,1,0,0,0,1,1,1,
                        1,1,1,0,1,1,1,1,
                        1,1,1,1,1,1,1,1,
                    ]
            },
            'text-tasks': {
                'type': 'text',
                'width': 10,
                'height': 8,
                'x': 17,
                'y': 1,
                'content': '%d' % self.tasks,
            },
            'text-name': {
                'type': 'text',
                'width': 32,
                'height': 8,
                'scrolling': True,
                'x': 0,
                'y': 9,
                'content': self.name,
            }
        }

    class Meta:
        verbose_name = _('Configuration : tâches')
        verbose_name_plural = _('Configurations : tâches')
