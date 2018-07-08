# coding: utf-8

from django.contrib import admin

from .models import Boite, Tile, TileApp

class BoiteAdmin(admin.ModelAdmin):
    readonly_fields = ('api_key','created_date', 'qrcode', 'last_activity', 'last_connection')

    list_display = ('name', 'user', 'screen', 'api_key', 'was_active_recently', 'sleep_time', 'wake_time', 'is_idle', 'last_activity', 'last_connection',)
    list_filter = ['last_activity', 'created_date']

    search_fields = ['name']

admin.site.register(Boite, BoiteAdmin)

class TileAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date']
    list_display = ('id', 'boite', 'duration', 'transition')

    search_fields = ['boite']

admin.site.register(Tile, TileAdmin)

class TileAppAdmin(admin.ModelAdmin):
    list_display = ('id', 'tile', 'x', 'y', 'content_object')

admin.site.register(TileApp, TileAppAdmin)
