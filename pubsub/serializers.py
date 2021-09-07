from rest_framework.serializers import ModelSerializer
from .models import TopicMessage

class TopicMessageSerializer(ModelSerializer):
    
    class Meta:
        model = TopicMessage
        fields = '__all__'