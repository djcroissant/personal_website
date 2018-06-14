from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.core import mail
from django.contrib import messages

from general.views import BioView
from general.forms import ContactForm


def setup_view(view, request, *args, **kwargs):
    """
    Mimic as_view() returned callable, but returns view instance.
    args and kwargs are the same you would pass to `reverse()`
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class BioViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_base_url_redirects_to_bio_page(self):
        url_path = "/bio"
        reverse_path = reverse("bio")
        self.assertEqual(reverse_path, url_path)

    def test_url_name_reverses_correctly(self):
        url_path = "/bio"
        reverse_path = reverse("bio")
        self.assertEqual(reverse_path, url_path)

    def test_view_uses_correct_template(self):
        request = self.factory.get("/fake/")
        response = BioView.as_view()(request)
        self.assertTrue("general/bio.html" in response.template_name)

    def test_valid_form_sends_email(self):
        """
        Ensures an email is sent when a valid contact form is submitted
        """
        request = self.factory.get("/fake/")
        kwargs = {}
        view = setup_view(BioView(), request, **kwargs)
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
