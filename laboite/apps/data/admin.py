from django.contrib import admin

from .models import AppData


class AppDataAdmin(admin.ModelAdmin):
    readonly_fields = ('data',)

    list_display = ('data', 'boite', 'enabled', 'created_date', 'last_activity')


admin.site.register(AppData, AppDataAdmin)
