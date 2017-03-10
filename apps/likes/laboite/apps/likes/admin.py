from django.contrib import admin

from .models import AppLikes


class AppLikesAdmin(admin.ModelAdmin):
    readonly_fields = ('likes',)

    list_display = ('page_name', 'likes', 'boite', 'enabled', 'get_app_dictionary', 'created_date', 'last_activity')


admin.site.register(AppLikes, AppLikesAdmin)
