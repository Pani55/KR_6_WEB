from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from mailing.forms import MailingForm, MessageForm
from mailing.models import Mailing, Message, Client, MailingTry
from mailing.services import get_uniq_clients_count, get_mailings_counts


# Create your views here.
class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uniq_clients'] = get_uniq_clients_count()
        context['mailings_count'], context[
            'active_mailings'] = get_mailings_counts()
        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing


class MailingDetailView(LoginRequiredMixin ,DetailView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Mailing(owner=self.request.user)
        return kwargs

    def get_success_url(self):
        return reverse('mailing:mailing_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.next_send_datetime = mailing.first_send_datetime
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['email', 'comment']

    def get_success_url(self):
        return reverse('mailing:client_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        client = form.save(commit=False)
        client.owner = self.request.user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['email', 'comment']

    def get_success_url(self):
        return reverse('mailing:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class MailingTryListView(LoginRequiredMixin, ListView):
    model = MailingTry
