from django.apps import AppConfig


class GodparentConfig(AppConfig):
    name = 'juntagrico_godparent'
    verbose_name = "Juntagrico Godparent"
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        # import to connect signals
        from .mailer import adminnotification, membernotification
