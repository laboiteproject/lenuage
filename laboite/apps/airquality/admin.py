from django.contrib import admin

from .models import AppAirQuality


class AppAirQualityAdmin(admin.ModelAdmin):
    readonly_fields = ['aqi_today']

    list_display = ('aqi_today', 'boite', 'enabled', 'created_date', 'last_activity')


admin.site.register(AppAirQuality, AppAirQualityAdmin)
