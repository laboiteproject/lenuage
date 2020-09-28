# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-24 09:31
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboite.apps.bikes', '0003_auto_20161224_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appbikes',
            name='provider',
            field=models.CharField(choices=[('star', 'Star - Rennes'), ('velib', "Vélib' - Paris")], help_text='Choisissez le service de vélos désiré', max_length=64, verbose_name='Fournisseur de données'),
        ),
    ]
