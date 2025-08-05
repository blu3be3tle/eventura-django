from django.db import models
from events.models import Event

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Event, related_name='users')

    def __str__(self):
        return self.name
