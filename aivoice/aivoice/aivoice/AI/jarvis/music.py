import os
import pygame
import random
from pygame import mixer
from Ear import listen  # Assuming this is your custom listen function
import threading
from Mouth import speak
# Initialize pygame and mixer
pygame.init()
mixer.init()

# Folder containing music files
MUSIC_FOLDER = r"C:\Users\adith\OneDrive\Desktop\songs"

def get_music_files():
    """Returns a list of available music files in the folder."""
    return [file for file in os.listdir(MUSIC_FOLDER) if file.endswith(('.mp3', '.wav', '.ogg', '.flac'))]

def play_music(song_name=None):
    """Plays a specific song by name or a random song if no name is given."""
    music_files = get_music_files()

    if not music_files:
        print("No music files found in the specified folder.")
        return

    # Select song
    if song_name:
        matching_files = [file for file in music_files if song_name.lower() in file.lower()]
        if not matching_files:
            print(f"No song found with the name '{song_name}'.")
            speak(f"No song found with the name '{song_name}'.")
            return
        selected_music = matching_files[0]  # Play the first matching file
    else:
        selected_music = random.choice(music_files)  # Play a random song

    music_path = os.path.join(MUSIC_FOLDER, selected_music)

    try:
        mixer.music.load(music_path)
        mixer.music.play()
        print(f"Playing: {selected_music}")

        # Wait while the music is playing
        while mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing music: {e}")

def stop_music():
    """Stop playing music."""
    mixer.music.stop()
    print("Music stopped.")
    speak("Music stopped.")

def listen_in_background():
    """Continuously listens for the word 'stop' in the background."""
    while True:
        command = listen().lower()  # Assume listen() function returns speech as text
        if "stop" or "stop it" in command:
            stop_music()
            print("🔴 Stopped the music from voice command.")
            break

if __name__ == "__main__":
    # Start the listening thread in the background
    listen_thread = threading.Thread(target=listen_in_background, daemon=True)
    listen_thread.start()
