from django.db import models
from django.contrib.auth.models import User, AbstractUser


# class CustomUser(AbstractUser):
#     pass

#     def __str__(self):
#         return self.username


class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='activity')
    status = models.CharField(max_length=20, default='offline')
    is_online = models.BooleanField(default=False)
    when = models.DateTimeField()

    def __str__(self):
        return self.user.username + ' is ' + self.status
