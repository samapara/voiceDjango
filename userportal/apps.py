from django.apps import AppConfig

from userportal.voice_backend.main import BackendHandler


class UserportalConfig(AppConfig):
    name = 'userportal'

    def ready(self):
        BackendHandler().test_models()
