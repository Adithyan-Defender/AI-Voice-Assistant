from django.urls import path
from .views import (
    start_jarvis_view,
    stop_jarvis_view,
    get_jarvis_output,
    ai_voice,
    add_jarvis_output,
)

app_name = "AI"  # Ensure this matches your Django project settings

urlpatterns = [
    path("ai-voice/", ai_voice, name="ai_voice"),
    path("ai-voice/start-jarvis/", start_jarvis_view, name="start_jarvis"),
    path("ai-voice/stop-jarvis/", stop_jarvis_view, name="stop_jarvis"),
    path("ai-voice/get-output/", get_jarvis_output, name="get_jarvis_output"),
    path("ai-voice/add-output/", add_jarvis_output, name="add_jarvis_output"),
]
