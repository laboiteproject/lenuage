# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.models import App, MINUTES

import asana
import unidecode


def get_projects(asana_personal_access_token):
    client = asana.Client.access_token(asana_personal_access_token)
    workspaces = client.workspaces.find_all()
    results = []

    try:
        for workspace in workspaces:
            projects = client.projects.find_all({'workspace': workspace['gid']})
            for project in projects:
                results.append({'id': project['gid'], 'name': project['name']})
    except Exception as e:
        pass

    results.sort(key=lambda proj: proj['name'])
    return results


class AppTasks(App):
    UPDATE_INTERVAL = 30 * MINUTES

    asana_personal_access_token = models.CharField(
        _("Clé d'API Asana"),
        help_text=_("Veuillez indiquer votre clé d'API personnelle Asana (Personal Access Token)"),
        max_length=64,
        default=None,
        null=True
    )
    asana_project_id = models.BigIntegerField(
        _('Identifiant projet Asana'),
        help_text=_("Veuillez indiquer l'identifiant du projet Asana dans lequel vous souhaitez travailler"),
        default=None,
        null=True
    )

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

        try:
            for task in tasks:
                if task['completed'] is False and task['assignee'] is not None:
                    if task['assignee']['gid'] == me.get('gid'):
                        uncompleted_tasks += 1
                        if uncompleted_tasks == 1:
                            self.name = str(unidecode.unidecode(task['name']))
        except Exception as e:
            pass
        self.tasks = uncompleted_tasks
        self.save()

    def _get_data(self):
        if self.tasks > 0:
            return {
                'width': 32,
                'height': 16,
                'data': [
                    {
                        'type': 'bitmap',
                        'width': 8,
                        'height': 8,
                        'x': 8,
                        'y': 0,
                        'color': 1,
                        'content': '0xfffffdb993c7efff'
                    },
                    {
                        'type': 'text',
                        'width': 10,
                        'height': 8,
                        'x': 17,
                        'y': 1,
                        'color': 3,
                        'font': 1,
                        'content': '%d' % self.tasks,
                    },
                    {
                        'type': 'text',
                        'width': 32,
                        'height': 8,
                        'x': 0,
                        'y': 9,
                        'color': 2,
                        'font': 1,
                        'content': self.name,
                    }
                ]
            }
        else:
            return {
                'width': 32,
                'height': 16,
                'data': [
                    {
                        'type': 'bitmap',
                        'width': 8,
                        'height': 8,
                        'x': 12,
                        'y': 4,
                        'color': 2,
                        'font': 1,
                        'content': '0xfffffdb993c7efff'
                    }
                ]
            }

    class Meta:
        verbose_name = _('Configuration : tâches')
        verbose_name_plural = _('Configurations : tâches')
