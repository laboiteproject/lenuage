from django.contrib import admin

from .models import AppBus


class AppBusAdmin(admin.ModelAdmin):
    readonly_fields = ('route0', 'departure0', 'route1', 'departure1', 'created_date', 'last_activity')

    list_display = ('boite', 'enabled', 'stop', 'route0', 'departure0', 'route1', 'departure1', 'get_app_dictionary', 'created_date', 'last_activity')


admin.site.register(AppBus, AppBusAdmin)
