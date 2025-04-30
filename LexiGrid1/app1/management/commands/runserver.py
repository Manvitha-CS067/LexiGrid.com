from django.contrib.sessions.models import Session
from django.core.management.commands.runserver import Command as RunserverCommand

class Command(RunserverCommand):
    def handle(self, *args, **options):
        # Clear all sessions before starting the server
        Session.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared all session data'))
        super().handle(*args, **options)