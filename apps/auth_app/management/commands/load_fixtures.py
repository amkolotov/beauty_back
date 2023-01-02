from decouple import config
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command

User = get_user_model()


class Command(BaseCommand):
    """Команда Django для заполнения бд данными из фикстур"""

    def handle(self, *args, **options):
        call_command('loaddata', 'fixtures/company.json')
        call_command('loaddata', 'fixtures/salons.json')
        call_command('loaddata', 'fixtures/salon_imgs.json')
        call_command('loaddata', 'fixtures/service_categories.json')
        call_command('loaddata', 'fixtures/specialists.json')
        call_command('loaddata', 'fixtures/services.json')
        call_command('loaddata', 'fixtures/work_imgs.json')
        call_command('loaddata', 'fixtures/sales.json')
        call_command('loaddata', 'fixtures/posts.json')
        call_command('loaddata', 'fixtures/users.json')
        call_command('loaddata', 'fixtures/reviews.json')
        call_command('loaddata', 'fixtures/orders.json')
