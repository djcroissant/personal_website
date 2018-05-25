from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages

from .forms import ContactForm

class HomeView(FormView):
    template_name = 'general/home.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Thanks for reaching out. Your message was sent successfully.')
        return super(HomeView, self).form_valid(form)
