# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models

from boites.models import Boite, App
from app_{{cookiecutter.app_name}} import settings


class App{{cookiecutter.app_model_name}}(App):
    ##### TODO: List your fields here.
    some_field_name = models.TextField(_(u'Some Field Name'), blank=True, null=True)

    def get_app_dictionary(self):
        if not self.enabled:
            return

        # we want to update every VALUES_UPDATE_INTERVAL minutes
        if timezone.now() <= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
            ##### TODO: Update the model field here: request some data, use Weboob...
            # response = requests.get("http://example.com")

            ##### TODO: Then store in the model.
            # self.some_field_name = response.text
            # self.save()
            pass

        return {'data': self.some_field_name}

    class Meta:
        verbose_name = _("Configuration : {{cookiecutter.app_verbose_name}}")
        verbose_name_plural = _("Configurations : {{cookiecutter.app_verbose_name}}")
