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

    api_key = models.CharField(_(u"Clé d'API"), max_length=36, unique=True)

    created_date = models.DateTimeField(_(u"Date de création"), auto_now_add=True)
    last_activity = models.DateTimeField(_(u"Dernière activité"), auto_now = True)
    last_connection = models.GenericIPAddressField(_(u"Dernière connexion"), protocol='both', unpack_ipv4=False, default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = uuid.uuid4()
        return super(Boite, self).save(*args, **kwargs)

    def belongs_to(self, user):
        return user == self.user

    def get_apps_dictionary(self):
        apps_dict = {}
        for model in apps.get_models():
            if issubclass(model, App):
                applications = model.objects.filter(boite=self)
                dicts = [a.get_app_dictionary() for a in applications]
                if dicts:
                    apps_dict[model._meta.app_label] = dicts

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
        # Child classes need to implement this.
        raise NotImplementedError

    class Meta:
        abstract = True
