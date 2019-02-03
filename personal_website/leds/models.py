from django.contrib.postgres.fields import JSONField
from django.db import models

class LedStripModel(models.Model):
  """
  Stores information for a users LED strip. 
  Initially, just a JSON value to return
  """
  name = models.CharField(max_length=200)
  data = JSONField()