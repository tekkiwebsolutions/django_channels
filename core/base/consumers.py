from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime

from user.models import UserActivity
from asgiref.sync import sync_to_async


def get_activity_dict(status, is_online, user_obj):
    return {'status': status, 'is_online': is_online,
            'user': user_obj, 'time': datetime.now()}


class UserActivityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'user_activity'

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
        data = get_activity_dict('offline', False, self.scope['user'])

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_user_activity',
                'is_activity': True,
                'user': data['user'].username,
                'status': data['status'],
                'is_online': data['is_online'],
                # 'when': data['time']
            }
        )

        await self.save_activity_to_db(data)

    async def receive(self, text_data):
        data = json.loads(text_data)
        data['user'] = self.scope['user']
        print(data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_user_activity',
                'is_activity': True,
                'user': data['user'].username,
                'status': data['status'],
                'is_online': data['is_online'],
                # 'when': data['time']
            }
        )

        await self.save_activity_to_db(data)

    @sync_to_async
    def save_activity_to_db(self, data):
        activity_obj = UserActivity.objects.filter(user=data['user']).first()

        if not activity_obj:
            UserActivity.objects.create(
                user=data['user'],
                status=data['status'],
                is_online=data['is_online'],
                when=data['time'],
            )
        else:
            activity_obj.status = data['status']
            activity_obj.is_online = data['is_online']
            activity_obj.when = data['time']
            activity_obj.save()

    async def send_user_activity(self, event):

        await self.send(text_data=json.dumps(
            {
                'is_activity': True,
                'user': event['user'],
                'status':  event['status'],
                'is_online': event['is_online'],
                # 'when': event['when']
            }
        ))
