from django.urls import path

from . import views

app_name = "about"
urlpatterns = [
    path("founder-bios", view=views.BioListView.as_view(), name="bios"),
]
