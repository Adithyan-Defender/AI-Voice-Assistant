import os
import subprocess
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# ✅ Path to your JARVIS script
JARVIS_SCRIPT = os.path.join(os.path.dirname(__file__), "jarvis", "main.py")

# ✅ Global process & message storage
jarvis_process = None
jarvis_messages = []

# ✅ Returns chat messages for frontend
@login_required
@csrf_exempt
def get_jarvis_output(request):
    return JsonResponse({"messages": jarvis_messages})


# ✅ Adds new chat message from frontend/backend
@login_required
@csrf_exempt
def add_jarvis_output(request):
    global jarvis_messages
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "")
        sender = data.get("sender", "JARVIS")

        # Prevent duplicates
        formatted = f"{sender}: {message}"
        if not jarvis_messages or jarvis_messages[-1] != formatted:
            jarvis_messages.append(formatted)

            # Limit to last 50 messages
            if len(jarvis_messages) > 50:
                jarvis_messages.pop(0)

    return JsonResponse({"status": "success"})


# ✅ Starts the JARVIS process
@login_required
def start_jarvis_view(request):
    global jarvis_process
    if jarvis_process is None or jarvis_process.poll() is not None:
        jarvis_process = subprocess.Popen(["python", JARVIS_SCRIPT])
        return JsonResponse({"status": "success", "message": "JARVIS started"})

    return JsonResponse({"status": "running", "message": "JARVIS is already running"})


# ✅ Stops JARVIS and resets message log
@login_required
def stop_jarvis_view(request):
    global jarvis_process, jarvis_messages
    if jarvis_process and jarvis_process.poll() is None:
        jarvis_process.terminate()
        jarvis_process = None

    jarvis_messages = ["System: JARVIS Stopped."]
    return JsonResponse({"status": "success", "message": "JARVIS stopped and messages cleared"})


# ✅ Renders the AI Voice Assistant page
@login_required
def ai_voice(request):
    return render(request, "screens/ai_voice.html", {"user": request.user})
