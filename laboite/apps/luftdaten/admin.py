from django.contrib import admin

from .models import AppLuftdaten


class AppLuftdatenAdmin(admin.ModelAdmin):
    readonly_fields = ['aqi']

    list_display = ('aqi', 'boite', 'enabled', 'created_date', 'last_activity')

admin.site.register(AppLuftdaten, AppLuftdatenAdmin)
