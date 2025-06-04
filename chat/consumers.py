from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.group_name = f"chat_{self.session_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        if content.get("type") == "user.message":
            response = {
                "type": "ai.message",
                "content": f"Echo: {content.get('content', '')}",
                "citations": [],
                "message_id": content.get("tmp_id"),
            }
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "chat.message", "message": response}
            )

    async def chat_message(self, event):
        await self.send_json(event["message"])
