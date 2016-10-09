# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.apps import apps
from datetime import timedelta

import uuid

@python_2_unicode_compatible
class Boite(models.Model):
    name = models.CharField(_(u"Nom"), help_text=_(u"Veuillez saisir un nom pour votre boîte"), max_length=32, default=_(u"Ma boîte"))
    user = models.ForeignKey(User, verbose_name = _(u"Utilisateur"))

    api_key = models.CharField(_(u"Clé d'API"), default=str(uuid.uuid4())[:8], max_length=8)

    created_date = models.DateTimeField(_(u"Date de création"), auto_now_add=True)
    last_activity = models.DateTimeField(_(u"Dernière activité"), auto_now = True)
    last_connection = models.GenericIPAddressField(_(u"Dernière connexion"), protocol='both', unpack_ipv4=False, default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    def belongs_to(self, user):
        return user == self.user

    def get_apps_dictionary(self):
        apps_dict = {}
        for app in apps.get_models():
            if str(app._meta.app_label).startswith('app'):
                app_dict = app.objects.get(boite = self).get_app_dictionary()
                apps_dict = dict(apps_dict, **app_dict)

        return apps_dict

    def was_active_recently(self):
        return self.last_activity >= timezone.now() - timedelta(minutes=2)

    was_active_recently.admin_order_field = 'last_activity'
    was_active_recently.boolean = True
    was_active_recently.short_description = _(u"Connectée ?")

class App(models.Model):
    boite = models.ForeignKey(Boite, verbose_name = _(u"Boîte"))

    enabled = models.BooleanField(_(u"App activée ?"), help_text=_(u"Indique si cette app est activée sur votre boîte"), default=True)

    created_date = models.DateTimeField(_(u"Date de création"), auto_now_add=True)
    last_activity = models.DateTimeField(_(u"Dernière activité"), auto_now = True)

    def get_app_dictionary(self):
        pass

    class Meta:
        abstract = True
