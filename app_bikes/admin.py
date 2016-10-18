from django.contrib import admin

from .models import AppBikes


class AppBikesAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'last_activity', 'nb_stands', 'nb_available', 'status')

    list_display = ('boite', 'enabled', 'get_app_dictionary', 'created_date', 'last_activity')


admin.site.register(AppBikes, AppBikesAdmin)
