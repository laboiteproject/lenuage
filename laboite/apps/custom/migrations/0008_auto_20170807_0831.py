# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-07 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboite.apps.custom', '0007_bitmap_app_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='appcustom',
            name='height',
            field=models.PositiveIntegerField(default=16, verbose_name="Hauteur de l'ic\xf4ne"),
        ),
        migrations.AddField(
            model_name='appcustom',
            name='width',
            field=models.PositiveIntegerField(default=16, verbose_name="Largeur de l'ic\xf4ne"),
        ),
    ]