from django.contrib import admin

from .models import AppParcel

class AppParcelAdmin(admin.ModelAdmin):
    readonly_fields = ('status', 'arrival', 'url', 'created_date', 'last_activity')

    list_display = ('boite', 'enabled', 'parcel', 'parcel_carrier', 'status', 'arrival', 'url', 'get_app_dictionary', 'created_date', 'last_activity')

admin.site.register(AppParcel, AppParcelAdmin)
