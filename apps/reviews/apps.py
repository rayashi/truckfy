from django.apps import AppConfig


class PersonasConfig(AppConfig):
    name = 'apps.reviews'

    def ready(self):
        import apps.reviews.signals
