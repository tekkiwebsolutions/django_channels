from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import json

from django.contrib.auth.models import User
from .models import SeenDetail, UserChatRoom, UserChatMessages
from django.db.models import Q
from base.utils import covert_date_to_string


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print(self.scope['url_route']['kwargs'], 'ss'*100)
        created_with = self.scope['url_route']['kwargs']['created_with']
        created_by = self.scope['url_route']['kwargs']['created_by']
        self.room_name = created_with.lower()+created_by.lower()
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', None)
        mark_as_read = data.get('mark_as_read', False)
        if message:
            # created_with = data['created_with']
            sent_by = data['sent_by']
            room = data['room']

            message_id = await self.save_message(sent_by, room, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    # 'created_with': created_with,
                    'sent_by': sent_by,
                    'room': room,
                    'id': message_id
                }
            )
        if mark_as_read:
            message_ids_list = data['messages_ids']
            seen_by_username = data['seen_by_user']

            seen_at = await self.mark_as_read(message_ids_list, seen_by_username)

            print('1'*250)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'seen_by_message',
                    'seen_by_username': seen_by_username,
                    'message_ids': message_ids_list,
                    'seen_at': seen_at,
                }
            )

    async def seen_by_message(self, event):
        seen_by_username = event['seen_by_username']
        message_ids = event['message_ids']
        seen_at = event['seen_at']

        await self.send(text_data=json.dumps({
            'mark_as_read': True,
            'seen_by_username': seen_by_username,
            'message_ids': message_ids,
            'seen_at': seen_at
            }))

    async def chat_message(self, event):
        message = event['message']
        sent_by = event['sent_by']
        room = event['room']
        id = event['id']

        await self.send(text_data=json.dumps({
            'message': message,
            # 'created_with': created_with,
            'sent_by': sent_by,
            'room': room,
            'id': id
        }))

    @sync_to_async
    def mark_as_read(self, messIds, read_by_username):
        user = User.objects.get(username=read_by_username)
        for messId in messIds:
            mess_obj = UserChatMessages.objects.get(id=messId)
            seen_detail_obj = SeenDetail.objects.create(user=user, message=mess_obj)
        seen_at = covert_date_to_string(seen_detail_obj.created_at)
        return seen_at

    @sync_to_async
    def save_message(self, sent_by, room, message):
        # created_with = User.objects.get(username=created_with)
        sent_by = User.objects.get(username=sent_by['username'])
        # reverse_name = created_by.username + '/' + created_with.username
        # room = UserChatRoom.objects.get(Q(slug=room), Q(
        #     reverse_name=reverse_name))
        room = UserChatRoom.objects.filter(Q(
            name=room, reverse_name='hthth', _connector=Q.OR
        )).first()
        message = UserChatMessages.objects.create(
            # sent_to=created_with,
            sent_by=sent_by,
            room=room,
            content=message,
        )
        return message.id 


class MarkAsRead(AsyncWebsocketConsumer):
    async def connect(self):
        created_with = self.scope['url_route']['kwargs']['created_with']
        created_by = self.scope['url_route']['kwargs']['created_by']
        self.room_name = created_with.lower()+created_by.lower()
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
