# coding: utf-8

from django.contrib import admin

from .models import Boite

class BoiteAdmin(admin.ModelAdmin):
    readonly_fields = ('api_key','created_date', 'qrcode', 'last_activity', 'last_connection')

    list_display = ('name', 'user', 'api_key', 'was_active_recently', 'get_apps_dictionary', 'last_activity', 'last_connection',)
    list_filter = ['last_activity', 'created_date']

    search_fields = ['name']

admin.site.register(Boite, BoiteAdmin)
