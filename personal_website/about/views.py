from django.shortcuts import render
from django.views.generic import ListView

from about.models import Bio


class BioListView(ListView):
  template_name = 'about/bios.html'
  model = Bio