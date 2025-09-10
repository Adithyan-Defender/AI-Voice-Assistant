import time
import pywhatkit as kt
import random
from DLG import playsong, playing_dlg
from Mouth import speak

def play_on_youtube(text, content_type="music"):
    """
    Plays a YouTube video or music based on user input.
    
    Parameters:
    - text (str): The search query for YouTube.
    - content_type (str): "music" for songs, "video" for any video. Default is "music".
    """

    if content_type.lower() == "music":
        playdlg = random.choice(playsong)
        speak(playdlg)  # Announce playing music
    else:
        speak(f"Playing the video: {text}")  # Announce playing video

    kt.playonyt(text)  # Open the video on YouTube
    time.sleep(3)

    if content_type.lower() == "music":
        playdlg = random.choice(playing_dlg)
        speak(playdlg + " " + text)  # Announce the song name


