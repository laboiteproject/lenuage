from django.contrib import admin

from .models import AppTraffic


class AppTrafficAdmin(admin.ModelAdmin):
    readonly_fields = ('trajectory_name', 'trip_duration')
    list_display = ('boite', 'enabled', 'start', 'dest', 'get_app_dictionary')


admin.site.register(AppTraffic, AppTrafficAdmin)
