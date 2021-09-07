from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MqttBrokerConsumer(AsyncWebsocketConsumer):
    
    def decode_message(self, text):
        return json.loads(text)
    
    def encode_message(self, data):
        return json.dumps(data)
    
    # this method is called when websocket connection is created
    async def connect(self):
        await self.accept()
    
    # this method is called when websocket receives a message
    async def receive(self, text_data):
        data = self.decode_message(text_data)
        
        if 'subscribe' in data:
            await self.channel_layer.group_add(
                data['subscribe'],
                self.channel_name
            )
        
        if 'publish' in data:
            await self.channel_layer.group_send(
                data['publish']['topic'],
                {
                    'type': 'publish.message',
                    'message': self.encode_message({
                        'message': data['publish']['message'],
                        'topic': data['publish']['topic']
                    })
                }
            )
    
    async def publish_message(self, event):
        await self.send(self.encode_message(event['message']))
    
    # this function is called when websocket connection is closed
    async def disconnect(self, code):
        print(f'websocket connection closed : -> {code} <-')
    