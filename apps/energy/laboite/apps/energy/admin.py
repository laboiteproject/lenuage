from django.contrib import admin

from .models import AppEnergy


class AppEnergyAdmin(admin.ModelAdmin):
    readonly_fields = ('power', 'day0', 'day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'created_date', 'last_activity')

    list_display = ('boite', 'enabled', 'power', 'get_app_dictionary', 'created_date', 'last_activity')


admin.site.register(AppEnergy, AppEnergyAdmin)
