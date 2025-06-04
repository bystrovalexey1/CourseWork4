from django.core.management.base import BaseCommand

from newsletters.models import Distribution
from newsletters.tasks import send_distribution_task


class Command(BaseCommand):
    help = "Sends a mailing by ID"

    def add_arguments(self, parser):
        parser.add_argument(
            "distribution_id", type=int, help="ID of the mailing to send"
        )

    def handle(self, *args, **options):
        distribution_id = options["distribution_id"]
        try:
            distribution = Distribution.objects.get(pk=distribution_id)
            send_distribution_task.delay(
                distribution.pk
            )  # Запускаем задачу Celery асинхронно
            self.stdout.write(
                self.style.SUCCESS(f'Успешно запущена рассылка "{distribution.pk}"')
            )
        except Distribution.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Рассылка "{distribution_id}" не найдена')
            )
