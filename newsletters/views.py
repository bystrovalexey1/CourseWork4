from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import request, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db import models
from django_apscheduler.models import DjangoJob

from newsletters.forms import RecipientForm, DistributionForm, MessageForm
from newsletters.models import Recipient, Message, Distribution, NewslettersAttempt


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Получатель успешно создан.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Ошибка создания получателя. Проверьте введенные данные."
        )
        return super().form_invalid(form)



class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'recipient_confirm_delete.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'recipient_detail.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Сообщение успешно создано.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Ошибка создания сообщения. Проверьте введенные данные."
        )
        return super().form_invalid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'message_confirm_delete.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'message_detail.html'


class DistributionCreateView(LoginRequiredMixin, CreateView):
    model = Distribution
    form_class = DistributionForm
    template_name = 'distribution_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        distribution = form.save()

        first_send_data = distribution.first_send_data
        last_send_data = distribution.last_send_data

        DjangoJob.objects.create(
            name=f"distribution_task_{distribution.pk}",
            task="distribution.tasks.schedule_distribution_wrapper",
            args=[str(distribution.pk)],
            next_run_time=first_send_data,
            end_datetime=last_send_data,
            replace_existing=True,
        )

        messages.success(self.request, "Рассылка успешно создана и запланирована.")
        return super().form_valid(form)


class DistributionUpdateView(LoginRequiredMixin, UpdateView):
    model = Distribution
    form_class = DistributionForm
    template_name = 'distribution_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class DistributionDeleteView(LoginRequiredMixin, DeleteView):
    model = Distribution
    template_name = 'distribution_confirm_delete.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class DistributionDetailView(LoginRequiredMixin, DetailView):
    model = Distribution
    template_name = 'distribution_detail.html'


class DistributionListView(LoginRequiredMixin, ListView):
    model = Distribution
    template_name = 'distribution_list.html'


class HomeListView(ListView):
    model = Distribution
    template_name = "home.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_distribution = Distribution.objects.count()
        active_distribution = Distribution.objects.filter(status="запущена").count()
        unique_recipient = Recipient.objects.values("email").distinct().count()
        context = {
            "total_distribution": total_distribution,
            "active_distribution": active_distribution,
            "unique_recipient": unique_recipient,
        }
        return context


class StartDistributionView(LoginRequiredMixin, View):
    def post(self, request, pk):
        distribution = get_object_or_404(Distribution, pk=pk, owner=request.user)

        if distribution.first_send_data <= timezone.now():
            messages.error(
                request, "Нельзя запустить рассылку, дата начала которой уже прошла"
            )
            return redirect("newsletters:distribution_list")

        distribution.status = "запущена"
        distribution.save()

        messages.success(request, f'Рассылка "{distribution.pk}" была запущена.')
        return redirect("newsletters:distribution_list")


@login_required
def distribution_reports(request):
    """
    Отображает отчеты о попытках рассылки для текущего пользователя.
    """

    distributions = Distribution.objects.filter(owner=request.user)

    newsletter_attempts = (
        NewslettersAttempt.objects.filter(distribution__in=distributions)
        .values("distribution")
        .annotate(
            total_attempts=Count("distribution"),
            successful_attempts=Count("distribution", filter=models.Q(attempt_status="успешно")),
            failed_attempts=Count("distribution", filter=models.Q(attempt_status="не успешно")),
        )
    )

    # Подготовьте словарь для учета количества попыток для каждой рассылки
    newsletter_stats = {attempt["distribution"]: attempt for attempt in newsletter_attempts}

    # Передача данных в шаблон
    context = {
        "distributions": distributions,
        "newsletter_stats": newsletter_stats,
    }
    return render(request, "distribution_reports.html", context)
