from django.contrib import admin

from .models import AppWeather

class AppWeatherAdmin(admin.ModelAdmin):
    readonly_fields = ('temperature_now', 'humidity_now', 'icon_now', 'created_date', 'last_modified')

    list_display = ('boite', 'enabled', 'city_name', 'temperature_now', 'humidity_now', 'icon_now', 'get_app_dictionary', 'created_date', 'last_modified')

admin.site.register(AppWeather, AppWeatherAdmin)
