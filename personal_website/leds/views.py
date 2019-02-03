from django.shortcuts import render
from django.views.generic import JsonReturnView

from leds.models import LedStripModel

class JsonReturnView(View):

    def get(self, request, *args, **kwargs):
        data={"hello": "goodbye"}
        return JsonResponse(data)
