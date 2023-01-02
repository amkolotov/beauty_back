from decouple import config
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Команда Django для создания суперпользователя"""

    def handle(self, *args, **options):
        username = config('ADMIN_USERNAME')
        email = config('ADMIN_EMAIL')
        password = config('ADMIN_PASSWORD')
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
