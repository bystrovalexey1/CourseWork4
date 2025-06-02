import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from newsletters.models import Distribution, NewslettersAttempt

logger = logging.getLogger(__name__)


@shared_task(bind=True, retry_backoff=True)
def send_distribution_task(self, distribution_id):
    """
    Рассылает электронные письма клиентам из списка рассылки.
    """
    distribution = Distribution.objects.get(pk=distribution_id)

    # Проверяем время отправки
    if distribution.status == "завершена":
        logger.info(f"Рассылка {distribution.pk} уже завершена.")
        return

    # Привлекаем клиентов для рассылки
    recipients = distribution.recipient.all()

    for recipient in recipients:
        try:
            send_mail(
                distribution.message.theme,
                distribution.message.text_letter,
                settings.EMAIL_HOST_USER,  # Отправляем письмо
                [recipient.email],  # Электронное письмо получателя
                fail_silently=False,
            )
            # Запишите успешную попытку
            NewslettersAttempt.objects.create(
                distribution=distribution,
                status="успешно",
                server_response="Письмо отправлено успешно!",
            )
            logger.info(f"Отправлено письмо на {recipient.email} {distribution.pk}")

        except Exception as e:
            # Запишите неудачную попытку
            NewslettersAttempt.objects.create(
                distribution=distribution, status="не успешно", server_response=str(e)
            )
            logger.error(
                f"Ошибка отправки на {recipient.email} {distribution.pk}: {e}"
            )
            raise self.retry(exc=e, countdown=60)  # Повторите попытку через 60 секунд

    distribution.status = "завершена"
    distribution.save()
    logger.info(f"Рассылка {distribution.pk} завершена.")


@shared_task(bind=False)
def schedule_mailing_wrapper(distribution_id):
    """Запускает задачу отправки рассылки асинхронно через Celery."""
    send_distribution_task.delay(distribution_id)