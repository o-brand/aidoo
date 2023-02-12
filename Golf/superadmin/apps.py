from django.apps import AppConfig


class SuperadminConfig(AppConfig):
    """This is the config class for the superadmin app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'superadmin'
