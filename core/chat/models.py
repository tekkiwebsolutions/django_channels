from django.db import models
from base.models import DateAndTimeStamp
from django.contrib.auth.models import User


class UserChatRoom(DateAndTimeStamp):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    reverse_name = models.CharField(max_length=250)
    created_by = models.ForeignKey(User, related_name='created_chat',
                                   on_delete=models.CASCADE)
    # created_with = models.ForeignKey(User, related_name='created_wit_chat',
    #                                  on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="chat_rooms")
    is_group = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserChatMessages(DateAndTimeStamp):
    room = models.ForeignKey(UserChatRoom, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.content


class SeenDetail(DateAndTimeStamp):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    message = models.ForeignKey(UserChatMessages, on_delete=models.CASCADE,
                                related_name='seen_details')
    is_recieved = models.BooleanField(default=False)
