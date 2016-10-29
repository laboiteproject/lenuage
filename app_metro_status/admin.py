from django.contrib import admin

from .models import AppMetroStatus

class AppMetroStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('failures',)

    list_display = ('boite', 'enabled', 'failures', 'get_app_dictionary', 'created_date', 'last_activity')

admin.site.register(AppMetroStatus, AppMetroStatusAdmin)
