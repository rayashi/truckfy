from django.apps import AppConfig


class PersonasConfig(AppConfig):
    name = 'apps.personas'

    def ready(self):
        import apps.personas.signals
