from django.apps import AppConfig
from django.db.models.signals import post_migrate


def populate_games(sender, **kwargs):
    from django.core.management import call_command
    call_command('populate_games')


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        post_migrate.connect(populate_games, sender=self)