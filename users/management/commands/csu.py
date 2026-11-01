from django.core.management import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Создание суперпользователя'

    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@example.com",
            username="admin",
            first_name="Admin",
            last_name="Admin",
            is_active=True,
            is_staff=True,
            is_superuser=True,
            role="admin",
        )
        user.set_password("0000")
        user.save()
        self.stdout.write(self.style.SUCCESS('Суперпользователь успешно создан!'))