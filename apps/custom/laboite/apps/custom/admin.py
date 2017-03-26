from django.contrib import admin

from .models import AppCustom


class AppCustomAdmin(admin.ModelAdmin):
    readonly_fields = ('icon',)

    list_display = ('message', 'icon', 'boite', 'enabled', 'get_app_dictionary', 'created_date', 'last_activity')


admin.site.register(AppCustom, AppCustomAdmin)
