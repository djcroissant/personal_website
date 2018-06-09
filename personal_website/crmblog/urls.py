from django.urls import path

from . import views

app_name = "crmblog"
urlpatterns = [
    path("", view=views.HomeView.as_view(), name="home"),
    path("archive", view=views.ArchiveView.as_view(), name="archive"),
]
