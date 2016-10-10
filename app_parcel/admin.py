from django.contrib import admin

from .models import AppParcel

class AppParcelAdmin(admin.ModelAdmin):
    readonly_fields = ('arrival', 'status','info', 'url', 'created_date', 'last_activity')

    list_display = ('boite', 'enabled', 'parcel', 'parcel_carrier', 'arrival', 'status', 'info', 'get_app_dictionary', 'created_date', 'last_activity')

admin.site.register(AppParcel, AppParcelAdmin)
