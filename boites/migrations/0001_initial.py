# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-21 20:41
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Boite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Ma bo\xeete', help_text='Veuillez saisir un nom pour votre bo\xeete', max_length=32, verbose_name='Nom')),
                ('api_key', models.CharField(max_length=36, unique=True, verbose_name="Cl\xe9 d'API")),
                ('qrcode', models.ImageField(upload_to='boites', verbose_name='QR code')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Date de cr\xe9ation')),
                ('last_activity', models.DateTimeField(auto_now=True, verbose_name='Derni\xe8re activit\xe9')),
                ('last_connection', models.GenericIPAddressField(blank=True, default=None, null=True, verbose_name='Derni\xe8re connexion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
    ]
