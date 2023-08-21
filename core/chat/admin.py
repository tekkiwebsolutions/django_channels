from django.contrib import admin
from .models import UserChatMessages, UserChatRoom, SeenDetail

admin.site.register(UserChatRoom)
admin.site.register(UserChatMessages)
admin.site.register(SeenDetail)
