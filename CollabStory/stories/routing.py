from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/story/(?P<story_id>\d+)/$', consumers.StoryConsumer.as_asgi()),
]
