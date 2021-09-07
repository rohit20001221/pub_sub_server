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
        # await self.send(text_data='')
        # await self.close()
        return
    
    # this function is called when websocket connection is closed
    async def disconnect(self, code):
        print(f'websocket connection closed : -> {code} <-')
    