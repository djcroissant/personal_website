from django.urls import path

from . import views

app_name = "leds"
urlpatterns = [
    path("json-data", view=views.JsonDataView.as_view(), name="json-data"),
    path("control-panel", view=views.ControlPanelView.as_view(), name="led-ui"),
    path("update-json-data", view=views.AjaxUpdateJsonDataView, name="update-json-data"),
]
