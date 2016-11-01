from django.contrib import admin

from .models import AppMessages

class AppMessagesAdmin(admin.ModelAdmin):
    readonly_fields = ('message', 'created_date', 'last_activity')

    list_display = ('boite', 'enabled', 'message', 'get_app_dictionary', 'created_date', 'last_activity')

admin.site.register(AppMessages, AppMessagesAdmin)
