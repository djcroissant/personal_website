from django.shortcuts import render
from django.views.generic import View, TemplateView, UpdateView
from django.http import JsonResponse, HttpResponse


from leds.models import LedStrip

class JsonDataView(View):
    def get(self, request, *args, **kwargs):
        data={"hello": "goodbye"}
        return JsonResponse(data)

class ControlPanelView(TemplateView):
  template_name = 'leds/control-panel.html'

# class AjaxUpdateJsonDataView(UpdateView):
#   model = LedStrip
#   def get_object(self, queryset=None):
#     print('hello view')
#     super(AjaxUpdateJsonDataView, self).get_object(queryset=None)

def AjaxUpdateJsonDataView(request):
    if request.is_ajax():
        message = "Yes, AJAX!"
        print("hi AJAX")
    else:
        message = "Not Ajax"
    return HttpResponse(message)