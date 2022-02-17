from django.apps import AppConfig


class ExtensionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'extensions'

    def ready(self):
        from jobs import updater
        updater.start()