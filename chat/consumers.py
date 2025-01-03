# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import GuideRequest
from django.utils import timezone
from datetime import timedelta


class GuideRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the current guide's ID (assuming the user is a guide)
        self.guide_id = self.scope['user'].id
        # Unique room group for each guide's requests
        self.room_group_name = f'guide_{self.guide_id}_requests'

        # Join the WebSocket group for this specific guide
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group when disconnected
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        request_id = data.get('request_id')

        # Process the request update based on action (accept, reject, timeout)
        try:
            guide_request = GuideRequest.objects.get(id=request_id)

            if action == 'accept':
                guide_request.status = 'accepted'
            elif action == 'reject':
                guide_request.status = 'rejected'
            elif action == 'timeout':
                guide_request.status = 'time_out'

            # Optionally set expiration time (if timeout or reject logic)
            if action == 'timeout':
                guide_request.expires_at = timezone.now()  # Immediate timeout

            guide_request.save()

            # Send the updated status to the group (guide)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'guide_request_status',  # Send status update to group
                    'status': guide_request.status,
                    'request_id': guide_request.id,
                    'expires_at': guide_request.expires_at.isoformat(),
                }
            )
        except GuideRequest.DoesNotExist:
            pass

    async def guide_request_status(self, event):
        # Send the updated status to the WebSocket client (guide)
        await self.send(text_data=json.dumps({
            'status': event['status'],
            'request_id': event['request_id'],
            'expires_at': event['expires_at'],
        }))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Define the room name for the chat (e.g., based on the request_id)
        self.room_name = self.scope['url_route']['kwargs']['request_id']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the room group (chat group for the specific request)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group when disconnected
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Send the message to the room group (chat group)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket (chat UI)
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
