from django.urls import path

from . import views

app_name = "crmblog"
urlpatterns = [
    path("", view=views.WebHomeView.as_view(), name="home"),
    path("archive", view=views.WebPostListView.as_view(), name="archive"),
    path("<slug:slug>", view=views.PostDetailView.as_view(), name="post_detail"),
]
