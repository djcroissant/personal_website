from django.shortcuts import render
from django.views.generic import ListView

from about.models import Bio


class BioListView(ListView):
  template_name = 'about/bios.html'
  model = Bio

  def get_queryset(self):
    queryset = super(BioListView, self).get_queryset()
    return queryset.order_by('created')