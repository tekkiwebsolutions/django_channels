from django.db import models
from django.contrib.auth.models import User
from base.models import DateAndTimeStamp


class Room(DateAndTimeStamp):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)


class Message(DateAndTimeStamp):
    room = models.ForeignKey(Room, related_name='messages',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages',
                             on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        ordering = ('created_at',)
