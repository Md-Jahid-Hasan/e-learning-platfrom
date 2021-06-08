import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from django.utils import timezone

from .models import ChatData


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Accept Connection"""
        self.user = self.scope['user']
        print(self.scope)
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        print(self.room_group_name)

        """Join Room group"""
        print(self.channel_name)
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # self.send(text_data=json.dumps({'message': message}))  # Sent message to websocket
        chat = await sync_to_async(ChatData.objects.create)(room_name=self.room_group_name, message=message,
                                                            user=self.user, date=now)
        print(chat)
        print(message, self.user.username, now)
        """send message to room group"""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
