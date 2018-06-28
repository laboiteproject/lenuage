from django.contrib import admin

from .models import AppBitmap, Bitmap


class AppBitmapAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'last_activity')

    list_display = ('id', 'width', 'height', 'boite', 'color', 'enabled', 'created_date', 'last_activity')


admin.site.register(AppBitmap, AppBitmapAdmin)

class BitmapAdmin(admin.ModelAdmin):
    list_display = ('id', 'app_id', 'bitmap', )

admin.site.register(Bitmap, BitmapAdmin)
