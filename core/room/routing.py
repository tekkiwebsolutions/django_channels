from django.urls import path
from . import consumers
from chat import consumers as chat_consumers
from base.consumers import UserActivityConsumer

websocket_urlpatterns = [
     path('ws/user_activity/', UserActivityConsumer.as_asgi()),
     path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
     path('ws/chat/<str:created_with>/<str:created_by>/',
          chat_consumers.ChatConsumer.as_asgi()),
     path('ws/chat/mark_as_read>/',
          chat_consumers.MarkAsRead.as_asgi()),
    ]
