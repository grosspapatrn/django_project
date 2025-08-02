from django.apps import AppConfig


class TaskmanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TaskManager'

    def ready(self):
        import TaskManager.signals