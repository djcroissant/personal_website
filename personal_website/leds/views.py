from django.shortcuts import render
from django.views.generic import View, TemplateView, UpdateView
from django.http import JsonResponse


from leds.models import LedStripModel

class JsonDataView(View):
    def get(self, request, *args, **kwargs):
        data={"hello": "goodbye"}
        return JsonResponse(data)

class ControlPanelView(TemplateView):
  template_name = 'leds/control-panel.html'

class AjaxUpdateJsonDataView(UpdateView):
  pass
  # import pdb
  # pdb.set_trace()
