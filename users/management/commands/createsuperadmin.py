from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            email="superadmin@superadmin.ru",
            first_name="superadmin",
            last_name="superadmin",
        )

        user.set_password("12345678aA")

        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(self.style.SUCCESS(f"Успешно создан суперадмин {user.email}"))
