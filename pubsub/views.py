from asgiref.sync import async_to_sync
import channels.layers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MqttRestAPI(APIView):
    
    channel_layer = channels.layers.get_channel_layer()
    
    def get(self, request, topic):
        async_to_sync((self.channel_layer.group_add))(topic, f'rest_{topic}')
        data = async_to_sync(self.channel_layer.receive)(f'rest_{topic}')
        return Response(data)
        
    
    def post(self, request, topic):
        async_to_sync((self.channel_layer.group_add))(topic, f'rest_{topic}')
        async_to_sync(self.channel_layer.group_send)(topic, {'type':'publish.message', 'message':{'topic':topic, 'message': request.data['value']}})
        
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)