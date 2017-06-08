from django.contrib import admin

from .models import AppWifi


class AppWifiAdmin(admin.ModelAdmin):
    readonly_fields = []
    list_display = ('boite', 'enabled', 'get_app_dictionary', 'created_date', 'last_activity')


admin.site.register(AppWifi, AppWifiAdmin)
