from django.urls import reverse
from django.test import TestCase, RequestFactory

from crmblog.views import HomeView
from crmblog.models import Post


def setup_view(view, request, *args, **kwargs):
    """
    Mimic as_view() returned callable, but returns view instance.
    args and kwargs are the same you would pass to `reverse()`
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class HomeViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        Post.objects.create(title="one")
        Post.objects.create(title="two")
        Post.objects.create(title="three")
        Post.objects.create(title="four")
        Post.objects.create(title="five")

    def test_url_name_reverses_correctly(self):
        url_path = "/crm/"
        reverse_path = reverse("crmblog:home")
        self.assertEqual(reverse_path, url_path)

    def test_view_uses_correct_template(self):
        request = self.factory.get("/fake/")
        response = HomeView.as_view()(request)
        self.assertTrue("crmblog/home.html" in response.template_name)

    def test_list_view_returns_last_four_posts(self):
        request = self.factory.get("/fake/")
        kwargs = {}
        view = setup_view(HomeView(), request, **kwargs)
        queryset = view.get_queryset()
        self.assertEqual(len(queryset), 4)
        self.assertTrue(len(Post.objects.all()) > 4)

    def test_queryset_contains_last_post_first(self):
        request = self.factory.get("/fake/")
        kwargs = {}
        view = setup_view(HomeView(), request, **kwargs)
        queryset = view.get_queryset()
        self.assertEqual(Post.objects.last(), queryset[0])
        self.assertTrue(Post.objects.get(title="one") not in queryset)
