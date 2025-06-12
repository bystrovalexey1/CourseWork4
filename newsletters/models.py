from django.db import models

from users.models import CustomUser


class Recipient(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="ФИО")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Укажите автора",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.email} - {self.name}"

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["id"]


class Message(models.Model):
    theme = models.CharField(max_length=20, verbose_name="Тема")
    text_letter = models.TextField(verbose_name="Текст письма")
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Укажите автора",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.theme} - {self.text_letter}"

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["id"]


class Distribution(models.Model):
    first_send_data = models.DateTimeField(verbose_name="дата первой отправки")
    last_send_data = models.DateTimeField(verbose_name="дата последней отправки")
    STATUS_CHOICES = [
        ("завершена", "Завершена"),
        ("создана", "Создана"),
        ("запущена", "Запущена"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="создана")
    message = models.ForeignKey(
        Message,
        verbose_name="Сообщение",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    recipient = models.ManyToManyField(Recipient, verbose_name="Получатели")
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Укажите автора",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.message} - {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["id"]


class NewslettersAttempt(models.Model):
    attempt_send_data = models.DateTimeField(
        auto_now=True, verbose_name="дата и время попытки"
    )
    STATUS_CHOICES = [
        ("успешно", "Успешно"),
        ("не успешно", "Не успешно"),
    ]
    attempt_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="успешно"
    )
    answer = models.TextField(verbose_name="Текст ответа от почтового сервера")
    distribution = models.ForeignKey(
        Distribution,
        verbose_name="Рассылка",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.attempt_send_data} - {self.attempt_status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["id"]
