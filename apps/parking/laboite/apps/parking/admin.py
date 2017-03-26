from django.contrib import admin

from .models import AppParking


class AppParkingAdmin(admin.ModelAdmin):
    readonly_fields = ('open', 'available', 'occupied')

    list_display = ('parking', 'open', 'available', 'occupied', 'boite', 'enabled', 'get_app_dictionary', 'created_date', 'last_activity')


admin.site.register(AppParking, AppParkingAdmin)
