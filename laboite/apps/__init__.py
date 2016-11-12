__import__('pkg_resources').declare_namespace(__name__)

from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "laboite"

    def ready(self):
        import_module("laboite.receivers")
