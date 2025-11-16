from django.apps import AppConfig


class ComponentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'components'

    def ready(self):
        """Import signal handlers when Django starts."""
        import components.metrics  # noqa: F401
