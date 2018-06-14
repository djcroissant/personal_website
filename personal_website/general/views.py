from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages

from .forms import ContactForm

class BioView(FormView):
    template_name = 'general/bio.html'
    form_class = ContactForm
    success_url = reverse_lazy('bio')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Thanks for reaching out. Your message was sent successfully.')
        return super(BioView, self).form_valid(form)
