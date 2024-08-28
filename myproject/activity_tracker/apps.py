from django.apps import AppConfig
import threading
from . import tasks


class ActivityTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'activity_tracker'
    
    def ready(self):
        thread = threading.Thread(target = tasks.start_services)
        thread.daemon = True
        thread.start()
