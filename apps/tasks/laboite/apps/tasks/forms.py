# coding: utf-8
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _

from .models import AppTasks, get_projects


class ProjectIdWidget(forms.Select):
    def enable(self):
        self.attrs.pop('disabled', None)

    def disable(self):
        self.attrs['disabled'] = True

    def load_project_ids(self, asana_personal_access_token):
        try:
            self.choices = [(proj['id'], proj['name']) for proj in get_projects(asana_personal_access_token)]
            self.enable()
            return True
        except:
            self.disable()
            return False


class TasksModelForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        super(TasksModelForm, self).__init__(*args, **kw)
        widget = self.fields['asana_project_id'].widget
        value = ''
        if 'asana_personal_access_token' in self.data and self.data['asana_personal_access_token']:
            value = self.data['asana_personal_access_token']
        elif self.instance is not None and self.instance.asana_personal_access_token:
            value = self.instance.asana_personal_access_token
        if value:
            if not widget.load_project_ids(value):
                self.errors['asana_personal_access_token'] = [_("Clé d'API invalide.")]
        else:
            widget.disable()

    class Meta:
        model = AppTasks
        fields = ('asana_personal_access_token', 'asana_project_id')
        widgets = {
            'asana_project_id': ProjectIdWidget()
        }

    class Media:
        js = ('js/app_tasks_form.js',)
