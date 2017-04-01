# coding: utf-8

from __future__ import unicode_literals
from datetime import timedelta
import logging
import StringIO
import uuid

from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import qrcode


logger = logging.getLogger('laboite.apps')


SECONDS = 1
MINUTES = 60
HOURS = 3600


@python_2_unicode_compatible
class Boite(models.Model):
    name = models.CharField(_(u'Nom'), help_text=_('Veuillez saisir un nom pour votre boîte'), max_length=32, default=_('Ma boîte'))
    user = models.ForeignKey(User, verbose_name=_('Utilisateur'))

    api_key = models.CharField(_("Clé d'API"), max_length=36, unique=True)

    qrcode = models.ImageField(_('QR code'), upload_to='boites')

    created_date = models.DateTimeField(_('Date de création'), auto_now_add=True)
    last_activity = models.DateTimeField(_('Dernière activité'), null=True)
    last_connection = models.GenericIPAddressField(_('Dernière connexion'), protocol='both', unpack_ipv4=False, default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.generate_api_key()
        return super(Boite, self).save(*args, **kwargs)

    def generate_api_key(self):
        self.api_key = uuid.uuid4()
        self.generate_qrcode()
        self.last_activity = timezone.now()

    def generate_qrcode(self):
        url = 'http://'
        url += str(Site.objects.get_current())
        url += '/boites/redirect/'
        url += str(self.api_key)
        img = qrcode.make(url)

        buffer = StringIO.StringIO()
        img.save(buffer)

        filename = 'qrcode-%s.png' % str(self.api_key)
        file_buffer = filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.len, None)
        self.qrcode.save(filename, filebuffer)

    def belongs_to(self, user):
        return user == self.user

    def get_apps_dictionary(self):
        apps_dict = {}
        for model in apps.get_models():
            if issubclass(model, App):
                applications = model.objects.filter(boite=self, enabled=True)
                dicts = filter(lambda r: r is not None, [a.get_app_dictionary() for a in applications])
                if dicts:
                    apps_dict[model.get_label()] = dicts
        return apps_dict

    def was_active_recently(self):
        return self.last_activity >= timezone.now() - timedelta(minutes=2)

    was_active_recently.admin_order_field = 'last_activity'
    was_active_recently.boolean = True
    was_active_recently.short_description = _('Connectée ?')


class App(models.Model):
    """Base app model"""
    UPDATE_INTERVAL = None  # Subclasses can redefine it as a number of seconds between updates

    boite = models.OneToOneField(Boite, verbose_name=_('Boîte'))
    created_date = models.DateTimeField(_('Date de création'), auto_now_add=True)
    enabled = models.BooleanField(_('App activée ?'), help_text=_('Indique si cette app est activée sur votre boîte'), default=True)
    last_activity = models.DateTimeField(_('Dernière activité'), null=True)

    @classmethod
    def get_label(cls):
        return cls._meta.app_label

    def should_update(self):
        """Is stored data outdated?
        If UPDATE_INTERVAL is None, we should update it everytime.
        If last_activity is None, that means app was never updated or last data retrieval failed
        Otherwise compute if data is outdated.
        """
        if self.UPDATE_INTERVAL is None or self.last_activity is None:
            return True
        return self.last_activity + timedelta(seconds=self.UPDATE_INTERVAL) < timezone.now()

    def update_data(self):
        """Retrieve external data (if needed) and store them"""
        pass

    def _get_data(self):
        """Must be implemented in subclasses, will return a dict from stored data"""
        raise NotImplementedError

    def get_data(self):
        """Convert stored data to dict, None if there was an error or if the app is disabled"""
        if self.last_activity is None or not self.enabled:
            return None
        return self._get_data()

    def get_app_dictionary(self):
        if self.should_update():
            try:
                self.update_data()
                self.last_activity = timezone.now()
            except:
                logger.exception('App {} data retrieval failed'.format(self.get_label()))
                self.last_activity = None
            self.save()
        return self.get_data()

    class Meta:
        abstract = True
