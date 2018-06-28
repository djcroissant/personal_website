from django.db import models
from django.utils.html import strip_tags

from autoslug import AutoSlugField

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from taggit.managers import TaggableManager

from general.models import TimeStampedModel


class Post(TimeStampedModel):
    title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, blank=True)
    photo = models.FileField(
        upload_to='static/images/crmblog/post_photos', blank=True)
    content = MarkdownxField(blank=True)
    slug = AutoSlugField(populate_from='title', blank=True)
    posted_date = models.DateTimeField(null=True)

    tags = TaggableManager()

    def __str__(self):
        return self.title

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
