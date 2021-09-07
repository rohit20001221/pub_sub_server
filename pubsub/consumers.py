from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import TopicMessage

class MqttBrokerConsumer(AsyncJsonWebsocketConsumer):
    
    @database_sync_to_async
    def update_topic_message(self, topic, message):
        if TopicMessage.objects.filter(topic=topic).exists():
            t = TopicMessage.objects.get(topic=topic)
            t.message = message
            t.save()
        else:
            TopicMessage.objects.create(
                topic=topic,
                message=message
            )
    
    # this method is called when websocket connection is created
    async def connect(self):
        await self.accept()
    
    
    # this method is called when websocket receives a message
    async def receive_json(self, content):
        data = content
        
        if 'subscribe' in data:
            await self.channel_layer.group_add(
                data['subscribe'],
                self.channel_name
            )
            
        if 'unsubscribe' in data:
            await self.channel_layer.group_discard(
                data['unsubscribe'],
                self.channel_name
            )
        
        if 'publish' in data:
            await self.channel_layer.group_send(
                data['publish']['topic'],
                {
                    'type': 'publish.message',
                    'message': {
                        'message': data['publish']['message'],
                        'topic': data['publish']['topic']
                    }
                }
            )
    
    async def publish_message(self, event):
        await self.send_json(event['message'])
        await self.update_topic_message(event['message']['topic'], event['message']['message'])    
    
    # this function is called when websocket connection is closed
    async def disconnect(self, code):
        print(f'websocket connection closed : -> {code} <-')
    