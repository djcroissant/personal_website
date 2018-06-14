from django.utils import timezone

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
        """
        Create 6 Post objects. The first five get tagged "web development"
        The last gets tagged with something else
        """
        Post.objects.create(title="one", posted_date=timezone.now())
        Post.objects.create(title="two", posted_date=timezone.now())
        Post.objects.create(title="three", posted_date=timezone.now())
        Post.objects.create(title="four", posted_date=timezone.now())
        Post.objects.create(title="five", posted_date=timezone.now())
        for p in Post.objects.all():
            p.tags.add("web development",)
        exclude=Post.objects.create(title="exclude", posted_date=timezone.now())
        exclude.tags.add("different tag")

    def test_url_name_reverses_correctly(self):
        url_path = "/blog/web-development"
        reverse_path = reverse("crmblog:webhome")
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
        self.assertEqual(Post.objects.filter(tags__name__in=["web development"]).last(), queryset[0])
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
        Post.objects.create(title="one", posted_date=timezone.now())
        Post.objects.create(title="two", posted_date=timezone.now())
        Post.objects.create(title="three", posted_date=timezone.now())
        Post.objects.create(title="four", posted_date=timezone.now())
        Post.objects.create(title="five", posted_date=timezone.now())
        for p in Post.objects.all():
            p.tags.add("web development",)
        exclude=Post.objects.create(title="exclude", posted_date=timezone.now())
        exclude.tags.add("different tag")

    def test_url_name_reverses_correctly(self):
        url_path = "/blog/web-development/archive"
        reverse_path = reverse("crmblog:archive")
        self.assertEqual(reverse_path, url_path)

    def test_view_uses_correct_template(self):
        request = self.factory.get("/fake/")
        response = WebPostListView.as_view()(request)
        self.assertTrue("crmblog/archive.html" in response.template_name)

    def test_list_view_returns_all_correctly_tagged_posts(self):
        request = self.factory.get("/fake/")
        kwargs = {}
        view = setup_view(WebPostListView(), request, **kwargs)
        queryset = view.get_queryset()
        self.assertEqual(len(queryset), 5)
        self.assertTrue(len(Post.objects.all()) == 6)

    def test_queryset_contains_last_post_first(self):
        request = self.factory.get("/fake/")
        kwargs = {}
        view = setup_view(WebPostListView(), request, **kwargs)
        queryset = view.get_queryset()
        self.assertEqual(Post.objects.filter(tags__name__in=["web development"]).last(), queryset[0])

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
        url_path = "/blog/a-test-post"
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
