from decouple import config
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from apps.schedule.models import Segment

User = get_user_model()


class Command(BaseCommand):
    """Команда Django для создания суперпользователя"""

    def handle(self, *args, **options):
        if not Segment.objects.exists():
            for i in range(1, 49):
                Segment.objects.create(number=i)
