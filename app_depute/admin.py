from django.contrib import admin

from .models import AppDepute

class AppDeputeAdmin(admin.ModelAdmin):
    readonly_fields = ('presencePercentage',)
    list_display = ('get_app_dictionary',)

admin.site.register(AppDepute, AppDeputeAdmin)
