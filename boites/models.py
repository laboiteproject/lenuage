# coding: utf-8

from __future__ import unicode_literals

from datetime import timedelta
from io import BytesIO
import logging
import uuid
import time

from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MaxValueValidator
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
    user = models.ForeignKey(User, verbose_name=_('Utilisateur'), on_delete=models.CASCADE)

    SCREEN_CHOICES = (
        (0, _('Écran monochrome 32×8')),
        (1, _('Écran monochrome 32×16')),
        (2, _('Écran bicolore 32×16')),
    )

    screen = models.PositiveSmallIntegerField(_("Type d'écran"), help_text=_("Veuillez sélectionner l'écran qui compose votre boîte"), choices=SCREEN_CHOICES, default=1)

    api_key = models.CharField(_("Clé d'API"), max_length=36, unique=True)

    qrcode = models.ImageField(_('QR code'), upload_to='boites')

    created_date = models.DateTimeField(_('Date de création'), auto_now_add=True)
    last_activity = models.DateTimeField(_('Dernière activité'), null=True)
    last_connection = models.GenericIPAddressField(_('Dernière connexion'), protocol='both', unpack_ipv4=False, default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_tiles(self):
        """Get only tiles that contain apps"""
        query = Tile.objects.filter(boite=self)
        query = query.annotate(cnt_apps=models.Count('tile_apps'))
        query = query.filter(cnt_apps__gt=0)
        return query.order_by('id')

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

        buffer = BytesIO()
        img.save(buffer)

        filename = 'qrcode-%s.png' % str(self.api_key)
        filebuffer = InMemoryUploadedFile(buffer, None, filename,
                                          'image/png', len(buffer.getvalue()), None)
        self.qrcode.save(filename, filebuffer)

    def belongs_to(self, user):
        return user == self.user

    def get_apps_dictionary(self):
        apps_dict = {}
        for model in apps.get_models():
            if issubclass(model, App):
                applications = model.objects.filter(boite=self, enabled=True)
                dicts = [a.get_app_dictionary() for a in applications]
                dicts = [dct for dct in dicts if dct is not None]
                if dicts:
                    apps_dict[model.get_label()] = dicts
        return apps_dict

    def was_active_recently(self):
        return self.last_activity >= timezone.now() - timedelta(minutes=2)

    was_active_recently.admin_order_field = 'last_activity'
    was_active_recently.boolean = True
    was_active_recently.short_description = _('Connectée ?')


class PushButton(models.Model):
    api_key = models.SlugField(_(u"IFTTT clé d'API"), help_text=_("Veuillez saisir ici votre clé IFTTT"))
    boite = models.OneToOneField(Boite, verbose_name=_('Boîte'), on_delete=models.CASCADE)

    last_triggered = models.DateTimeField(_('Dernière activité'), null=True)

    def was_triggered_recently(self):
        return self.last_activity >= timezone.now() - timedelta(minutes=2)

    was_triggered_recently.admin_order_field = 'last_triggered'
    was_triggered_recently.boolean = True
    was_triggered_recently.short_description = _('Bouton appuyé récemment ?')


class App(models.Model):
    """Base app model"""
    UPDATE_INTERVAL = None  # Subclasses can redefine it as a number of seconds between updates

    boite = models.ForeignKey(Boite, verbose_name=_('Boîte'), on_delete=models.CASCADE)
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


class Tile(models.Model):
    TRANSITION_CHOICES = (
        (0, _('Aucune')),
        (1, _('Fondu')),
        (2, _('Défilement ←')),
        (3, _('Défilement →')),
        (4, _('Défilement ↑')),
        (5, _('Défilement ↓')),
    )

    boite = models.ForeignKey(Boite, on_delete=models.CASCADE)
    brightness = models.PositiveSmallIntegerField(_("Luminosité de la tuile"), help_text=_("Veuillez saisir la luminosité souhaitée pour cette tuile"), default=15, validators=[MaxValueValidator(15)])
    duration = models.PositiveSmallIntegerField(_("Durée d'affichage de la tuile"), help_text=_("Veuillez saisir une durée durant laquelle la tuile sera affichée (en millisecondes)"), default=5000)
    transition = models.PositiveSmallIntegerField(_('Transition'), help_text=_("Veuillez sélectionner la transition que vous souhaitez pour passer à la prochaine tuile"), choices=TRANSITION_CHOICES, default=0)
    created_date = models.DateTimeField(_('Date de création'), auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def get_data(self):
        apps = TileApp.objects.filter(tile=self)
        items = []
        for app in apps:
            items+=app.get_data()

        tile = {
            'id': self.id,
            'duration': self.duration,
            'brightness': self.brightness,
            'transition': self.transition,
            'items': items,
        }

        return tile

    def get_last_activity(self):
        last_activity = None
        for app in self.tile_apps.all():
            try:
                app.content_object.get_app_dictionary()
                app_last_activity = app.content_object.last_activity
                if app_last_activity is not None:
                    # Convert to UTC
                    app_last_activity = timezone.localtime(app_last_activity,
                                                           timezone.utc)
                # Keep it if it is greater than last_activity
                if last_activity is None or app_last_activity > last_activity:
                    last_activity = app_last_activity
            except AttributeError:
                logger.exception('App {} may not exist'.format(
                    app.content_object))

        if last_activity is None:
            return 0
        # Convert to integer number of seconds since epoch
        return int(time.mktime(last_activity.timetuple()))

    class Meta:
        verbose_name = _('Tuile')
        verbose_name_plural = _('Tuiles')


class TileApp(models.Model):
    tile = models.ForeignKey(Tile, on_delete=models.CASCADE, verbose_name=_('Tuile'), related_name='tile_apps')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("Type d'app"))
    object_id = models.PositiveIntegerField(verbose_name=_("Identifiant de l'app"))
    content_object = GenericForeignKey('content_type', 'object_id')
    x = models.SmallIntegerField(_('Position x'), help_text=_("Veuillez indiquer la position en x de l'app sur la tuile (en pixels)"), default=0)
    y = models.SmallIntegerField(_('Position y'), help_text=_("Veuillez indiquer la position en y de l'app sur la tuile (en pixels)"), default=0)

    def get_data(self):
        app = self.content_object.get_data()

        shifted_items = []
        for item in app.get('data'):
            shifted_item = {}
            for key, value in item.items():
                if key == 'x':
                    value += self.x
                if key == 'y':
                    value += self.y
                shifted_item[key] = value
            shifted_items.append(shifted_item)

        return shifted_items

    class Meta:
        verbose_name = _('App')
        verbose_name_plural = _('Apps')
