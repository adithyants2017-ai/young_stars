from django.apps import AppConfig


class ClubAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'club_app'

    def ready(self):
        import club_app.signals
