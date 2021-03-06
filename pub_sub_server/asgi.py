"""
ASGI config for pub_sub_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack

from pubsub.router import routes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pub_sub_server.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(), # <- for the http protocol 
    'websocket': AuthMiddlewareStack(routes)
})
