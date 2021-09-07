from channels.routing import URLRouter
from django.urls import path

from pubsub.consumers import MqttBrokerConsumer

routes = URLRouter([
    path('mqtt', MqttBrokerConsumer.as_asgi()),
])