from django.contrib import admin

from .models import AppCoffees


class AppCoffeesAdmin(admin.ModelAdmin):
    readonly_fields = ('daily', 'monthly',)

    list_display = ('daily', 'monthly', 'boite', 'enabled', 'get_app_dictionary', 'created_date', 'last_activity')


admin.site.register(AppCoffees, AppCoffeesAdmin)
