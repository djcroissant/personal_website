from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from personal_website.crmblog import views as crmblog_views

urlpatterns = [
    path("", crmblog_views.BlogHomeView.as_view(), name="home"),
    path(
        "leds/",
        include("personal_website.leds.urls", namespace="leds"),
    ),
    path(
        "blog/",
        include("personal_website.crmblog.urls", namespace="crmblog"),
    ),
    path(
        "about/",
        include("personal_website.about.urls", namespace="about"),
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path(
        "users/",
        include("personal_website.users.urls", namespace="users"),
    ),
    path("accounts/", include("allauth.urls")),
    re_path(r'^markdownx/', include('markdownx.urls')),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
