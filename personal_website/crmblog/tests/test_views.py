from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.core import mail
from django.contrib import messages

from crmblog.views import WebHomeView, WebPostListView, PostDetailView
from crmblog.models import Post
from crmblog.forms import ContactForm


def setup_view(view, request, *args, **kwargs):
    """
    Mimic as_view() returned callable, but returns view instance.
    args and kwargs are the same you would pass to `reverse()`
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class WebHomeViewTests(TestCase):
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
        response = WebHomeView.as_view()(request)
        self.assertTrue("crmblog/home.html" in response.template_name)

    def test_list_view_returns_last_four_posts(self):
        request = self.factory.get("/fake/")
        kwargs = {}
        view = setup_view(WebHomeView(), request, **kwargs)
        queryset = view.get_queryset()
        self.assertEqual(len(queryset), 4)
        self.assertTrue(len(Post.objects.all()) > 4)

    def test_queryset_contains_last_post_first(self):
        request = self.factory.get("/fake/")
        kwargs = {}
        view = setup_view(WebHomeView(), request, **kwargs)
        queryset = view.get_queryset()
        self.assertEqual(Post.objects.last(), queryset[0])
        self.assertTrue(Post.objects.get(title="one") not in queryset)

    def test_valid_form_sends_email(self):
        """
        Ensures an email is sent when a valid contact form is submitted
        """
        request = self.factory.get("/fake/")
        kwargs = {}
        view = setup_view(WebHomeView(), request, **kwargs)
        form = ContactForm({
            'name': "name",
            'email': "e@mail.com",
            'subject': "subject",
            'message': "message",
        })
        form.is_valid()

        # Following block addresses issue with unittests not knowing
        # MessageMiddleware is installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = view.form_valid(form)
        assert len(mail.outbox) == 1


class WebPostListViewTests(TestCase):
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
        url_path = "/crm/archive"
        reverse_path = reverse("crmblog:archive")
        self.assertEqual(reverse_path, url_path)

    def test_view_uses_correct_template(self):
        request = self.factory.get("/fake/")
        response = WebPostListView.as_view()(request)
        self.assertTrue("crmblog/archive.html" in response.template_name)

    def test_list_view_returns_all_posts(self):
        request = self.factory.get("/fake/")
        kwargs = {}
        view = setup_view(WebPostListView(), request, **kwargs)
        queryset = view.get_queryset()
        self.assertEqual(len(queryset), 5)
        self.assertTrue(len(Post.objects.all()) == 5)

    def test_queryset_contains_last_post_first(self):
        request = self.factory.get("/fake/")
        kwargs = {}
        view = setup_view(WebPostListView(), request, **kwargs)
        queryset = view.get_queryset()
        self.assertEqual(Post.objects.last(), queryset[0])

    def test_valid_form_sends_email(self):
        """
        Ensures an email is sent when a valid contact form is submitted
        """
        request = self.factory.get("/fake/")
        kwargs = {}
        view = setup_view(WebPostListView(), request, **kwargs)
        form = ContactForm({
            'name': "name",
            'email': "e@mail.com",
            'subject': "subject",
            'message': "message",
        })
        form.is_valid()

        # Following block addresses issue with unittests not knowing
        # MessageMiddleware is installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = view.form_valid(form)
        assert len(mail.outbox) == 1


class PostDetailViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(title="a test post")

    def test_url_name_reverses_correctly(self):
        url_path = "/crm/a-test-post"
        reverse_path = reverse("crmblog:post_detail", kwargs={'slug': self.post.slug})
        self.assertEqual(reverse_path, url_path)

    def test_view_uses_correct_template(self):
        request = self.factory.get("/fake/")
        response = PostDetailView.as_view()(request, slug=self.post.slug)
        self.assertTrue("crmblog/post_detail.html" in response.template_name)

    def test_valid_form_sends_email(self):
        """
        Ensures an email is sent when a valid contact form is submitted
        """
        request = self.factory.get("/fake/")
        kwargs = {'slug': self.post.slug}
        view = setup_view(PostDetailView(), request, **kwargs)
        form = ContactForm({
            'name': "name",
            'email': "e@mail.com",
            'subject': "subject",
            'message': "message",
        })
        form.is_valid()

        # Following block addresses issue with unittests not knowing
        # MessageMiddleware is installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = view.form_valid(form)
        assert len(mail.outbox) == 1
