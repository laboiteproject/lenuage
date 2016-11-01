# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from boites.models import App

class AppMessages(App):
    message = models.TextField(_(u"Message"), help_text=_(u"Veuillez indiquer le message pour votre boîte (max. 140 caractères)"), max_length=140, default="", blank=True)

    def get_app_dictionary(self):
        if self.enabled:
            return {'message': self.message}

    class Meta:
        verbose_name = _("Configuration : messages")
        verbose_name_plural = _("Configurations : messages")
