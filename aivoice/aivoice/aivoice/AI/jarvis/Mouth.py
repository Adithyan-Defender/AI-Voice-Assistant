import asyncio
import edge_tts
import pygame
import threading
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor


# Initialize pygame mixer
pygame.mixer.init()

# Voice option for English
VOICE = "en-US-AriaNeural"

# Background event loop for async TTS processing
executor = ThreadPoolExecutor(max_workers=2)
loop = asyncio.new_event_loop()

def start_background_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Start async loop in background thread
threading.Thread(target=start_background_loop, daemon=True).start()

# Global variable to track current speech playback
current_sound = None

async def stream_audio(text: str) -> BytesIO:
    """Convert text to speech and return an in-memory audio buffer."""
    buffer = BytesIO()
    communicate = edge_tts.Communicate(text, VOICE)
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buffer.write(chunk["data"])

    buffer.seek(0)
    return buffer

def play_audio(buffer: BytesIO):
    """Play audio from memory buffer and wait until playback is done."""
    global current_sound

    try:
        current_sound = pygame.mixer.Sound(buffer)
        current_sound.play()

        # Wait until playback is finished
        while pygame.mixer.get_busy():
            pygame.time.wait(100)  # Reduce CPU load
    except Exception as e:
        print(f"Playback error: {e}")
    finally:
        buffer.close()
        current_sound = None

def stop():
    """Immediately stops any ongoing speech playback."""
    global current_sound

    if current_sound:
        current_sound.stop()  # Stop playing immediately
        pygame.mixer.stop()  # Stop all audio channels
        print("Speech stopped.")

def speak(text: str):
    """Speak text using edge TTS (English Only)."""
    async def async_wrapper():
        try:
            buffer = await stream_audio(text)
            await loop.run_in_executor(executor, play_audio, buffer)
        except Exception as e:
            print(f"Speech error: {e}")

    # Run the async function in the background
    future = asyncio.run_coroutine_threadsafe(async_wrapper(), loop)
    future.result()  # Wait for completion before exiting
