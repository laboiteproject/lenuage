from django.contrib import admin

from .models import AppCustom, Bitmap


class AppCustomAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'last_activity')

    list_display = ('id', 'width', 'height', 'boite', 'enabled', 'get_app_dictionary', 'created_date', 'last_activity')


admin.site.register(AppCustom, AppCustomAdmin)

class BitmapAdmin(admin.ModelAdmin):
    list_display = ('id', 'app_id', 'bitmap', )

admin.site.register(Bitmap, BitmapAdmin)
