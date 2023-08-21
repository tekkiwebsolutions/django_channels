from django.conf.urls import url
from . import consumers

websocket_urlpatterns = url('ws/chat/<str:created_with>/<str:created_by>/',
                             consumers.ChatConsumer.as_asgi()),
