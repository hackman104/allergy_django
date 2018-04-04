import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Link(models.Model):
    restaurant_name = models.CharField(max_length=200)
    rest_link = models.CharField(max_length=200)
    add_date = models.DateTimeField('date added')

    def __str__(self):
        return self.restaurant_name

class Request(models.Model):
    request_name = models.CharField(max_length=200)
    request_link = models.CharField(max_length=200, blank=True, null=True)
    request_date = models.DateTimeField('date requested', blank=True, default=timezone.now)

    def __str__(self):
        return self.request_name

    def was_requested_recently(self):
        return self.request_date >= timezone.now() - datetime.timedelta(days=1)
