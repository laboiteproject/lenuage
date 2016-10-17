from django.contrib import admin

from .models import App{{cookiecutter.app_model_name}}

class App{{cookiecutter.app_model_name}}Admin(admin.ModelAdmin):
    readonly_fields = []

    list_display = ('boite', 'enabled', 'get_app_dictionary', 'created_date', 'last_activity')

admin.site.register(App{{cookiecutter.app_model_name}}, App{{cookiecutter.app_model_name}}Admin)
