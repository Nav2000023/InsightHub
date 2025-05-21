from django.apps import AppConfig


class InsightHubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'insight_hub'
    verbose_name = "Insights Hub"
    # label="insight_hub_app"

    def ready(self):
        import insight_hub.signals
