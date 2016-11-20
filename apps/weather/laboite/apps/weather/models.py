# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models

from datetime import timedelta
import pyowm

from boites.models import Boite, App
from . import settings

class AppWeather(App):
    city_name = models.CharField(_(u"Ville"), help_text=_(u"Veuillez saisir la ville où se trouve votre boîte"), max_length=64, default=_(u"Paris"))

    temperature_now = models.PositiveSmallIntegerField(_(u"Température actuelle"), null=True)
    humidity_now = models.PositiveSmallIntegerField(_(u"Humidité actuelle"), null=True)

    ICON_CHOICES = (
        (0, "Temps clair"),
        (1, "Nuages"),
        (2, "Pluie"),
        (3, "Brouillard"),
        (4, "Neige"),
    )
    icon_now = models.PositiveSmallIntegerField(_(u"Icône"), choices=ICON_CHOICES, default=1)

    def get_app_dictionary(self):
        if self.enabled:
            # we wan't to update every VALUES_UPDATE_INTERVAL minutes
            if self.temperature_now is None or timezone.now() >= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
                # pyowm examples : https://github.com/csparpa/pyowm#examples
                owm = pyowm.OWM(settings.OWM_APIKEY)

                # Search for current weather in city_name
                observation = owm.weather_at_place(self.city_name)
                weather = observation.get_weather()

                # Weather details
                temperatures = weather.get_temperature('celsius')

                self.temperature_now = temperatures['temp']
                self.humidity_now = weather.get_humidity()
                self.icon_now = self.convert_owm_icon(weather.get_weather_icon_name())

                self.save()

            return {'temperature_now': self.temperature_now, 'humidity_now' : self.humidity_now, 'icon_now': self.icon_now}

    def convert_owm_icon(self, owm_icon):
        # clouds
        icon = "1"
        owm_icon = owm_icon[:3]

        # clear sky
        if owm_icon == "01" or owm_icon == "01":
            icon = "0"
        # rain
        elif owm_icon == "09" or owm_icon == "10" or owm_icon == "11":
            icon = "2"
        # mist
        elif owm_icon == "50":
            icon = "3"
        # snow
        elif owm_icon == "13":
            icon = "4"

        return icon

    class Meta:
        verbose_name = _("Configuration : météo")
        verbose_name_plural = _("Configurations : météo")
