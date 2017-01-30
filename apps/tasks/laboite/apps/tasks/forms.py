from django import forms

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
        except:
            self.disable()


class TasksModelForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        super(TasksModelForm, self).__init__(*args, **kw)
        widget = self.fields['asana_project_id'].widget
        if self.instance is not None and self.instance.asana_personal_access_token:
            widget.load_project_ids(self.instance.asana_personal_access_token)
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
