from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse


from leds.models import LedStripModel

class JsonReturnView(View):
    def get(self, request, *args, **kwargs):
        data={"hello": "goodbye"}
        return JsonResponse(data)
