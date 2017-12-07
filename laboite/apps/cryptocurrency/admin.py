from django.contrib import admin

from .models import AppCryptocurrency


class AppCryptocurrencyAdmin(admin.ModelAdmin):
    readonly_fields = ('value', 'created_date', 'last_activity')

    list_display = ('cryptocurrency', 'currency', 'value', 'boite', 'enabled', 'created_date', 'last_activity')


admin.site.register(AppCryptocurrency, AppCryptocurrencyAdmin)
