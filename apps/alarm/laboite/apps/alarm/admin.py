from django.contrib import admin

from .models import AppAlarm


class AppAlarmAdmin(admin.ModelAdmin):
    list_display = ('heure', 'minutes')


admin.site.register(AppAlarm, AppAlarmAdmin)
