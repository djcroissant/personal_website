from django.urls import path

from . import views

app_name = "leds"
urlpatterns = [
    path("json-return", view=views.JsonReturnView.as_view(), name="json"),
]
