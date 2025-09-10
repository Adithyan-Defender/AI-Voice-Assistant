import threading
import time  
import requests
import os
import builtins  
from _intregation_automation import Automation
from Brain import brain, stop_generation  
from DLG import *
from welcome_greatings import *
from wish_greatings import *
from battery_plug_check import *
from battery_alert import *
from Ear import listen
from check_online_offline_status import *
from integration import play_on_youtube, handle_crypto_commands  
from Mouth import speak
# ✅ Corrected: Define stop_flag as threading.Event()
stop_flag = threading.Event()

# Django API endpoint to send messages
DJANGO_API_URL = "http://localhost:8000/ai/ai-voice/add-output/"  

# Store original print before overriding it
original_print = builtins.print  

def send_to_django(text, sender="JARVIS"):
    """Sends messages to Django for display in the chatbox."""
    try:
        requests.post(DJANGO_API_URL, json={"message": text, "sender": sender})
    except requests.exceptions.RequestException:
        pass  


def speak(text):
    """Send JARVIS' response to chatbox."""
    print(f"JARVIS: {text}")  
    send_to_django(text, sender="JARVIS")

def stop_speaking():
    """Stop ongoing speech."""
    try:
        from Mouth import stop
        stop()  
    except ImportError:
        pass  

def clear_output():
    """Clears terminal output and resets chatbox."""
    os.system('cls' if os.name == 'nt' else 'clear')
    send_to_django("__clear__")  
    time.sleep(0.5)  

def listen_and_interrupt():
    """Listens for 'stop' while JARVIS is speaking/responding."""
    while True:
        text = listen().lower().strip()
        if "stop" in text:
            stop_flag.set()  # ✅ Stop current generation
            stop_generation()  
            stop_speaking()
            clear_output()  
            speak("Alright, stopping.")  
            stop_flag.clear()  # ✅ Allow JARVIS to continue listening
            return  # ✅ Go back to listening without stopping JARVIS

def process_command(text):
    """Processes user command and sends output in full sentences only if it contains 'jarvis' or 'jarvisvis'."""
    stop_flag.clear()  # ✅ Allow command processing again
    send_to_django(text, sender="User")  
    
    listen_thread = threading.Thread(target=listen_and_interrupt, daemon=True)
    listen_thread.start()

    # ✅ YouTube Commands
    if "play video on youtube" in text:
        query = text.replace("play video on youtube", "").strip()
        play_on_youtube(query, content_type="video")
        return
    elif "play song on youtube" in text or "play music on youtube" in text:
        query = text.replace("play song on youtube", "").replace("play music on youtube", "").strip()
        play_on_youtube(query, content_type="music")
        return

    handle_crypto_commands(text)

    # ✅ Only send to brain() if it contains 'jarvis' or 'jarvisvis'
    if "jarvis" in text.lower() or "jarvisvis" in text.lower():
        response_text = brain(text)
        send_to_django(response_text, sender="JARVIS")


def stop_jarvis():
    """Stops JARVIS, clears messages, and resets output."""
    stop_flag.set()
    stop_speaking()
    stop_generation()
    
    send_to_django("__clear__")  # ✅ Signal frontend to clear chatbox
    time.sleep(0.5)  # ✅ Prevents immediate reloading of messages

def comain():
    """Continuously listens for commands and processes them."""
    while True:
        text = listen().lower().strip()  
        text = text.replace("jar", "jarvis")
        
        send_to_django(text, sender="User")

        Automation(text)
        Greating(text)

        if text in bye_key_word:
            speak(random.choice(res_bye))
            stop_jarvis()  
            break
        elif "jarvis" or "jarvisvis" in text:
            process_command(text)  
            time.sleep(2)  

def main():
    """Waits for wake-up command then starts JARVIS."""
    while True:
        wake_cmd = listen().lower().strip()
        if wake_cmd in wake_key_word:
            welcome()
            comain()
            time.sleep(3)  

def jarvis():
    """Runs multiple background processes."""
    threads = [
        threading.Thread(target=main, daemon=True),
        threading.Thread(target=battery_alert, daemon=True),
        threading.Thread(target=check_plugin_status, daemon=True),
        threading.Thread(target=realtime_online_checker, daemon=True),
    ]

    for t in threads:
        t.start()
    
    while True:
        time.sleep(1)  

if __name__ == "__main__":
    jarvis()
