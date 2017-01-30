from django.contrib import admin

from .models import AppTasks


class AppTasksAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'tasks', 'created_date', 'last_activity')

    list_display = ('boite', 'enabled', 'name', 'tasks', 'get_app_dictionary', 'created_date', 'last_activity')

    exclude = ('asana_project',)


admin.site.register(AppTasks, AppTasksAdmin)
