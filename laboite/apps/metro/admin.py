from django.contrib import admin

from .models import AppMetro


class AppMetroAdmin(admin.ModelAdmin):
    readonly_fields = ('failure', 'recovery_time', 'created_date', 'last_activity')

    list_display = ('boite', 'enabled', 'failure', 'recovery_time', 'get_app_dictionary', 'created_date', 'last_activity')


admin.site.register(AppMetro, AppMetroAdmin)
