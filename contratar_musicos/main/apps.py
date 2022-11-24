from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'contratar_musicos.main'

    def ready(self):
        import contratar_musicos.main.signals
