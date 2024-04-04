from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from ffinderapp import consumers
from ffinderapp.views import ChatConsumerView

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
    path('chat/', ChatView.as_view(), name='chat'),
    path('ws/chat/', ChatConsumerView.as_view(), name='chat_consumer'),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})