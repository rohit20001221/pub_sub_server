from django.db import models

# Create your models here.
class TopicMessage(models.Model):
    topic = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    
    def __str__(self):
        return self.topic