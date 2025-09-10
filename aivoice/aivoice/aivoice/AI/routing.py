from django.urls import re_path
from AI.consumer import JarvisConsumer

websocket_urlpatterns = [
    re_path(r"ws/jarvis/$", JarvisConsumer.as_asgi()),
]
