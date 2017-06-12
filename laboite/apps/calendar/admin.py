from django.contrib import admin

from .models import AppCalendar


class AppCalendarAdmin(admin.ModelAdmin):
    readonly_fields = ('dtstart', 'summary', 'created_date', 'last_activity')

    list_display = ('boite', 'enabled', 'dtstart', 'summary', 'get_app_dictionary', 'created_date', 'last_activity')


admin.site.register(AppCalendar, AppCalendarAdmin)
