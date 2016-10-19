# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from datetime import timedelta


from boites.models import App

class AppAlarm(App):
    H_CHOICES = (
        ("00", _(u"00")),
        ("01", _(u"01")),
        ("02", _(u"02")),
        ("03", _(u"03")),
        ("04", _(u"04")),
        ("05", _(u"05")),
        ("06", _(u"06")),
        ("07", _(u"07")),
        ("08", _(u"08")),
        ("09", _(u"09")),
        ("10", _(u"10")),
        ("11", _(u"11")),
        ("12", _(u"12")),
        ("13", _(u"13")),
        ("14", _(u"14")),
        ("15", _(u"15")),
        ("16", _(u"16")),
        ("17", _(u"17")),
        ("18", _(u"18")),
        ("19", _(u"19")),
        ("20", _(u"20")),
        ("21", _(u"21")),
        ("22", _(u"22")),
        ("23", _(u"23")),
    )

    heure = models.CharField(_(u"Heure"), help_text=_(u"Veuillez saisir l'heure de votre alarme"), max_length=32,default=_(u"00"), choices=H_CHOICES)

    M_CHOICES = (
        ("00", _(u"00")),
        ("05", _(u"05")),
        ("10", _(u"10")),
        ("15", _(u"15")),
        ("20", _(u"20")),
        ("25", _(u"25")),
        ("30", _(u"30")),
        ("35", _(u"35")),
        ("40", _(u"40")),
        ("45", _(u"45")),
        ("50", _(u"50")),
        ("55", _(u"55")),
    )

    minutes = models.CharField(_(u"Minutes"), help_text=_(u"Veuillez saisir les minutes de votre alarme"), max_length=32, default=_(u"00"),choices=M_CHOICES)



    def get_app_dictionary(self):


        return {'alarm': self.heure+":"+self.minutes,}

    class Meta:
        verbose_name = _("Configuration : alarm")
        verbose_name_plural = _("Configurations : alarm")
