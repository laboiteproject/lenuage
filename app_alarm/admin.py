from django.contrib import admin

from .models import AppAlarm

class AppAlarmAdmin(admin.ModelAdmin):
    readonly_fields = ()

    list_display = ('heure','minutes',)

admin.site.register(AppAlarm, AppAlarmAdmin)
