from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import TopicMessageSerializer
from .models import TopicMessage

import channels.layers
from asgiref.sync import async_to_sync


class MqttRestGetAPI(RetrieveAPIView):
    serializer_class = TopicMessageSerializer
    queryset = TopicMessage.objects.all()
    lookup_field = 'topic'
    
class MqttRestPostAPI(APIView):
    channel_layer = channels.layers.get_channel_layer()
    
    def post(self, request, topic):
        async_to_sync(self.channel_layer.group_add)(topic, 'rest')
        async_to_sync(self.channel_layer.group_send)(topic, {'type':'publish.message', 'message': {'topic':topic, 'message': request.data['value']}})
        async_to_sync(self.channel_layer.group_discard)(topic, 'rest')
        
        if TopicMessage.objects.filter(topic=topic).exists():
            t = TopicMessage.objects.get(topic=topic)
            t.message = request.data['value']
            t.save()
        else:
            TopicMessage.objects.create(
                topic=topic,
                message=request.data['value']
            )
        
        
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)