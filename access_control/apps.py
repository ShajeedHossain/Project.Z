from django.apps import AppConfig


class AccessControlConfig(AppConfig):
    name = 'access_control'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import access_control.signals  