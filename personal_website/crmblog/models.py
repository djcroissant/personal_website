from django.db import models
from django.utils.html import strip_tags
from django.conf import settings

from autoslug import AutoSlugField

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from taggit.managers import TaggableManager


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    "created" and "modified" fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, blank=True)
    photo = models.FileField(
        upload_to='static/images/crmblog/post_photos')
    content = MarkdownxField(blank=True)
    slug = AutoSlugField(populate_from='title', blank=True)
    posted_date = models.DateTimeField(null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, on_delete=models.SET_NULL)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    # def save_model(self, request, obj, form, change):
    #   if not obj.pk:
    #       # Only set added_by during the first save.
    #       obj.author = request.user
    #   super().save_model(request, obj, form, change)

    @property
    def excerpt(self):
        """
        Returns the first 10 words of the post content.
        First convert markdown to html
        Then removes all html formatting
        """
        excerpt_list = strip_tags(self.content).split(" ")
        excerpt = " ".join(strip_tags(markdownify(self.content)).split(" ")[:10])
        if len(excerpt_list) > 10:
            excerpt += " ..."
        return excerpt

    @property
    def formatted_markdown(self):
        return markdownify(self.content)

    @property
    def pretty_date(self):
        return self.posted_date.date().strftime('%B %d, %Y')
