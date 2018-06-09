from django.urls import path

from . import views

app_name = "crmblog"
urlpatterns = [
    path("", view=views.HomeView.as_view(), name="home"),
    path("archive", view=views.PostListView.as_view(), name="archive"),
    path("<slug:slug>", view=views.PostDetailView.as_view(), name="post_detail"),
]
