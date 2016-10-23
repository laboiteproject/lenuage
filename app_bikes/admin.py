from django.contrib import admin

from .models import AppBikes
from .forms import BikeModelForm


class AppBikesAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'last_activity', 'slots', 'bikes', 'status')

    list_display = ('boite', 'enabled', 'get_app_dictionary', 'created_date', 'last_activity')

    exclude = ('station',)

    form = BikeModelForm


admin.site.register(AppBikes, AppBikesAdmin)
