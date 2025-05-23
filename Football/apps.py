from django.apps import AppConfig


class FootballConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"
    name = "Football"

    def ready(self):
        import Football.signals
