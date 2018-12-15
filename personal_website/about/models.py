from django.db import models
from django.conf import settings

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    "created" and "modified" fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Bio(TimeStampedModel):
    person = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, on_delete=models.SET_NULL)
    photo = models.FileField(
        upload_to='static/images/about/bios')
    content = MarkdownxField(blank=True)

    def __str__(self):
        return self.person.name

    @property
    def formatted_markdown(self):
        return markdownify(self.content)
