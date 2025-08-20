from django.apps import AppConfig


class News_PortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'News_Portal'
    def ready(self):
        import News_Portal.signals






