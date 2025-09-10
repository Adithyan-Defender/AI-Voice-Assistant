import json
from channels.generic.websocket import AsyncWebsocketConsumer

class JarvisConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("jarvis_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("jarvis_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({"message": data["message"]}))

    async def send_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))