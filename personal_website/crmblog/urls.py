from django.urls import path

from . import views

app_name = "crmblog"
urlpatterns = [
    path("blog-demo", view=views.BlogDemoView.as_view(), name="blog_demo"),
    path("blog-home", view=views.BlogHomeView.as_view(), name="blog_home"),
    path("web-development", view=views.WebHomeView.as_view(), name="webhome"),
    path("web-development/archive", view=views.WebPostListView.as_view(), name="archive"),
    # slug routing needs to be listed last or else django trys to read
    # the url as a slug, but doesn't find matching object, and throws error
    path("<slug:slug>", view=views.PostDetailView.as_view(), name="post_detail"),
]
