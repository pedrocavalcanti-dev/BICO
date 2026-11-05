from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import AuthThrottleBucket


class Command(BaseCommand):
    help = "Remove contadores de autenticação expirados há mais de 48 horas."

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(hours=48)
        deleted, _details = AuthThrottleBucket.objects.filter(window_started_at__lt=cutoff).delete()
        self.stdout.write(f"Contadores expirados removidos: {deleted}.")
