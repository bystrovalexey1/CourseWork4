from django.db import models


class Recipient(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="ФИО")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f'{self.email} - {self.name}'

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["id"]


class Message(models.Model):
    theme = models.CharField(max_length=20, verbose_name="Тема")
    text_letter = models.TextField(verbose_name="Текст письма")

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["id"]


class Distribution(models.Model):
    first_send_data = models.DateTimeField(auto_now=True, verbose_name="дата первой отправки")
    last_send_data = models.DateTimeField(auto_now=True, verbose_name="дата последней отправки")
    STATUS_CHOICES = [
        ('завершена', 'Завершена'),
        ('создана', 'Создана'),
        ('запущена', 'Запущена'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='создана')
    message = models.ForeignKey(
        Message,
        verbose_name='Сообщение',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    recipient = models.ManyToManyField(Recipient, verbose_name="Получатели")

    def __str__(self):
        return f'{self.message} - {self.status}'

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["id"]
