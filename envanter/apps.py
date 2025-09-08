# envanter/apps.py

from django.apps import AppConfig

class EnvanterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'envanter'

    # Bu metodu ekliyoruz
    def ready(self):
        import envanter.signals