from django.db import models
from django.utils import timezone
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='events'
    )
    image = models.ImageField(upload_to='event_images/',  blank=True, null=True, default='default.jpg')

    def __str__(self):
        return self.name

    def is_past(self):
        event_datetime = datetime.combine(self.date, self.time)
        return event_datetime < timezone.now().replace(tzinfo=None)
