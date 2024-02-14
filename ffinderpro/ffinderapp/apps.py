from django.apps import AppConfig


class FfinderappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ffinderapp"

def ready(self):
    from .signals import create_profile