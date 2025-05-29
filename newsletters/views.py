from django.core.exceptions import PermissionDenied
from django.http import request, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from newsletters.models import Recipient, Message, Distribution


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'newsletters/recipient_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'newsletters/recipient_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'newsletters/recipient_confirm_delete.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'newsletters/recipient_detail.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = RecipientForm
    template_name = 'newsletters/message_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = RecipientForm
    template_name = 'newsletters/message_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'newsletters/message_confirm_delete.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'newsletters/message_detail.html'


class DistributionCreateView(LoginRequiredMixin, CreateView):
    model = Distribution
    form_class = DistributionForm
    template_name = 'newsletters/distribution_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class DistributionUpdateView(LoginRequiredMixin, UpdateView):
    model = Distribution
    form_class = DistributionForm
    template_name = 'newsletters/distribution_form.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class DistributionDeleteView(LoginRequiredMixin, DeleteView):
    model = Distribution
    template_name = 'newsletters/distribution_confirm_delete.html'
    success_url = reverse_lazy('newsletters:distribution_list')


class DistributionDetailView(LoginRequiredMixin, DetailView):
    model = Distribution
    template_name = 'newsletters/distribution_detail.html'


class DistributionListView(LoginRequiredMixin, ListView):
    model = Distribution
    template_name = 'newsletters/distribution_list.html'

    def get_queryset(self):
        queryset = cache.get('distribution_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('distribution_queryset', queryset, 60 * 15)
        return queryset
