import requests
import ollama
import datetime
import pickle
import os
import re  
import threading
from Mouth import speak

# ✅ Use threading.Event() instead of a boolean for proper control
stop_flag = threading.Event()

# ✅ Free API (DeepInfra)
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
API_KEY = "Bearer oAy8mBEvxmCxsPcY4fhetTAnFarjeR2U"  # Replace with actual key
HISTORY_FILE = "conversation_history.pkl"
api_limit_reached = False  # Global flag for API status

# ✅ System prompt
SYSTEM_PROMPT = "You are JARVIS, an advanced AI assistant built by Adithyan, a BCA student. Be concise, helpful, and friendly."
INTRO_MESSAGE = "Hello! I am JARVIS, your AI assistant, designed and built by Adithyan, a BCA student. How can I assist you today?"

# ✅ Django API URL for sending messages
DJANGO_API_URL = "http://localhost:8000/ai/ai-voice/add-output/"

# ✅ Initialize conversation history globally
conversation_history = []

def send_to_django(text, sender="JARVIS"):
    """Sends messages to Django WebSocket/chatbox."""
    try:
        requests.post(DJANGO_API_URL, json={"message": text, "sender": sender})
    except requests.exceptions.RequestException:
        pass  

# ✅ Load conversation history from file
def load_history():
    global conversation_history  # ✅ Ensure history is loaded globally
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "rb") as f:
                conversation_history = pickle.load(f)
                if not isinstance(conversation_history, list):
                    conversation_history = []
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            conversation_history = []
    else:
        conversation_history = []

# ✅ Save conversation history
def save_history():
    with open(HISTORY_FILE, "wb") as f:
        pickle.dump(conversation_history, f)

# ✅ Initialize conversation history
load_history()
if not conversation_history or conversation_history[0]["role"] != "system":
    conversation_history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})

# ✅ Prepare messages (Fix for missing function)
def prepare_messages():
    return [conversation_history[0]] + conversation_history[-10:]  # ✅ Keep last 10 exchanges

# ✅ Validate user input (Fix for missing function)
def is_valid_user_input(text):
    return not bool(re.search(r"(/|\\|python|exe|OneDrive|AppData|Users)", text, re.IGNORECASE))

# ✅ AI Chat Response (Cloud API)
def chat_with_cloud(prompt):
    global conversation_history, api_limit_reached  # ✅ Declare `conversation_history` as global
    if not is_valid_user_input(prompt):
        return "I cannot process system commands. Please ask a regular question. 😊"

    headers = {"Authorization": API_KEY, "Content-Type": "application/json"}
    conversation_history.append({"role": "user", "content": prompt})

    try:
        response = requests.post(API_URL, headers=headers, json={
            "model": "meta-llama/Meta-Llama-3-8B-Instruct",
            "messages": prepare_messages(),
            "temperature": 0.7,
            "max_tokens": 150
        }, timeout=10)

        if response.status_code == 200:
            bot_response = response.json()["choices"][0]["message"]["content"]
            conversation_history.append({"role": "assistant", "content": bot_response})
            save_history()
            return bot_response
        elif response.status_code in [401, 403, 429]:
            api_limit_reached = True
            return chat_with_local(prompt)
    except (requests.exceptions.RequestException, ConnectionError):
        api_limit_reached = True
        return chat_with_local(prompt)

# ✅ Local Chat (Fix for missing function)
def chat_with_local(prompt):
    global conversation_history  # ✅ Declare `conversation_history` as global
    if not is_valid_user_input(prompt):
        return "I cannot process system commands. Please ask a regular question. 😊"
    
    conversation_history.append({"role": "user", "content": prompt})
    
    response = ollama.chat(
        model="llama3",
        messages=prepare_messages(),
        options={
            "num_ctx": 256,
            "num_predict": 150,
            "temperature": 0.7,
            "low_vram": True
        }
    )

    if stop_flag.is_set():
        return "🔴 Process stopped."

    bot_response = response['message']['content']
    conversation_history.append({"role": "assistant", "content": bot_response})
    save_history()
    return bot_response

# ✅ Fixed Brain Function
def brain(text):
    """Processes user input and returns AI response properly."""
    global stop_flag
    if not text:
        return "Please provide input."

    stop_flag.clear()

    # ✅ Process AI response
    response = chat_with_cloud(text) if not api_limit_reached else chat_with_local(text)

    if stop_flag.is_set():
        return "🔴 Process stopped."

    # ✅ Remove unwanted "Ah, human" phrases
    response = re.sub(r"\bAh, human,\s*", "", response).strip()

    # ✅ Send response to frontend
    send_to_django(response)

    # ✅ Speak response in a separate thread (prevents delays)
    speak_thread = threading.Thread(target=speak, args=(response,))
    speak_thread.start()
    
    return response

# ✅ Stop ongoing response
def stop_generation():
    """Stops ongoing text generation properly and resumes listening."""
    global stop_flag
    stop_flag.set()
    send_to_django("Speech stopped.", sender="System")
