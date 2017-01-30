# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-30 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboite.apps.traffic', '0004_auto_20170129_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='apptraffic',
            name='mode',
            field=models.CharField(choices=[('driving', 'En voiture'), ('walking', 'A pied'), ('bicycling', 'A v\xe9lo'), ('transit', 'En transport en commun')], default='driving', max_length=32, null=True, verbose_name='Mode de transport'),
        ),
    ]
