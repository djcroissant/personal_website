from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin
from django.contrib import messages

from crmblog.models import Post
from .forms import ContactForm


class EmailFormListView(FormMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super(EmailFormListView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Thanks for reaching out. Your message was sent successfully.')
        return super(EmailFormListView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class HomeView(EmailFormListView):
    model = Post
    template_name = 'crmblog/home.html'
    form_class = ContactForm
    success_url = reverse_lazy('crmblog:home')

    def get_queryset(self):
        queryset = super(HomeView, self).get_queryset()
        return queryset.order_by('-created')[:4]     # Only need the 4 most recent posts

class ArchiveView(EmailFormListView):
    model = Post
    template_name = 'crmblog/archive.html'
    form_class = ContactForm
    success_url = reverse_lazy('crmblog:home')

    def get_queryset(self):
        queryset = super(ArchiveView, self).get_queryset()
        return queryset.order_by('-created')
