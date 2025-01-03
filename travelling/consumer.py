# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GuideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Logic for connecting, e.g., join a group for guide updates
        self.room_group_name = 'guide_updates_group'  # A group for all guide updates
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group when the WebSocket disconnects
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Receive data and broadcast it to the group
        data = json.loads(text_data)
        guide_id = data['guide_id']
        is_occupied = data['is_occupied']

        # Send the updated guide status to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'guide_status_update',
                'guide_id': guide_id,
                'is_occupied': is_occupied
            }
        )

    async def guide_status_update(self, event):
        # Broadcast the guide status update to the WebSocket
        await self.send(text_data=json.dumps({
            'guide_id': event['guide_id'],
            'is_occupied': event['is_occupied']
        }))
