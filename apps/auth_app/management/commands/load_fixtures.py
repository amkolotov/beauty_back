from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command

from apps.salon.models import CompanyInfo

User = get_user_model()


class Command(BaseCommand):
    """Команда Django для заполнения бд данными из фикстур"""

    def handle(self, *args, **options):
        if not CompanyInfo.objects.exists():
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
