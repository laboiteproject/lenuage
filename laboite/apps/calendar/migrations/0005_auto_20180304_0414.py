# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-04 03:14
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laboite.apps.calendar', '0004_auto_20170129_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appcalendar',
            name='boite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boites.Boite', verbose_name='Boîte'),
        ),
    ]
