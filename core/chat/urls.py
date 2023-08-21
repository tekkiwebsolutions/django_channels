from django.urls import path
from .views import chats, chat, mark_as_read, get_messages


urlpatterns = [
    path('', chats, name='chats'),
    path('ajax/mark_as_read', mark_as_read, name='mark_as_read'),
    path('get_messages/<str:room>', get_messages, name='get_messages'),
    path('<str:created_with>/<str:created_by>', chat, name='chat'),

]
