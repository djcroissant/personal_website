from django.db import models

from general.models import TimeStampedModel

class Post(TimeStampedModel):
    title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    photo = models.FileField(upload_to='static/images/crmblog/post_photos')
    content = TextField
