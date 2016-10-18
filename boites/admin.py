# coding: utf-8

from django.contrib import admin

from .models import Boite

class BoiteAdmin(admin.ModelAdmin):
    readonly_fields = ('api_key','created_date', 'last_activity', 'last_connection')

    list_display = ('name', 'user', 'was_active_recently', 'get_apps_dictionary', 'last_activity', 'last_connection', 'api_key')
    list_filter = ['last_activity', 'created_date']

    search_fields = ['name']

admin.site.register(Boite, BoiteAdmin)
