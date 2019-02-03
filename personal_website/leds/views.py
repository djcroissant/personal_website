from django.shortcuts import render
from django.views.generic import View, TemplateView, UpdateView
from django.http import JsonResponse, HttpResponse

from leds.models import LedStrip

import json

# class JsonDataView(View):
#     def get(self, request, *args, **kwargs):
#         data={"hello": "goodbye"}
#         return JsonResponse(data)

def JsonDataView(request):
  if request.method == "GET":
    obj=LedStrip.objects.get(pk=1)
    return JsonResponse(obj.data)

class ControlPanelView(TemplateView):
  template_name = 'leds/control-panel.html'

# class AjaxUpdateJsonDataView(UpdateView):
#   model = LedStrip
#   def get_object(self, queryset=None):
#     print('hello view')
#     super(AjaxUpdateJsonDataView, self).get_object(queryset=None)

def AjaxUpdateJsonDataView(request):
    if request.is_ajax() and request.method == 'POST':
      r = request.POST.dict()
      data = {
        "r": r["r"],
        "g": r["g"],
        "b": r["b"], 
      }
      # UPDATE: GIVE LEDSTRIP A NAME AND CONNECT IT TO A USER
      obj=LedStrip.objects.get(pk=1)
      obj.data=data
      obj.save()
      return JsonResponse({'result':'All is well on the luminous front'})
    else:
      return JsonResponse({'result':'Something went terribly wrong!'})
