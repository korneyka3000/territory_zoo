from django.apps import AppConfig
from django.db.models.signals import post_save,pre_save


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    # def ready(self):
    #     # Implicitly connect signal handlers decorated with @receiver.
    #     from . import signals
    #     # Explicitly connect a signal handler.
    #     pre_save.connect(signals.my_handler)
