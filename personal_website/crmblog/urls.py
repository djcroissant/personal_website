from django.urls import path

from . import views

app_name = "crmblog"
urlpatterns = [
    path("web-development", view=views.WebHomeView.as_view(), name="webhome"),
    path("web-development/archive", view=views.WebPostListView.as_view(), name="archive"),
    path("projects", view=views.ProjectListView.as_view(), name="projects"),
    # slug routing needs to be listed last or else django trys to read
    # the url as a slug, but doesn't find matching object, and throws error
    path("<slug:slug>", view=views.PostDetailView.as_view(), name="post_detail"),
]
