from check_temperature import *
from CHECK_SPEED import *
from check_online_offline_status import *
from music import *  
from CLOCK import *
from find_my_ip import *
from Ear import *
def Function_cmd(text):
    if "check internet speed" in text or "check internet test" in text or "speed test" in text:
        check_internet_speed()
    
    elif "are you there" in text or "hello there" in text:
        internet_status()
    
    elif "check temperature" in text or "temperature" in text:
        Temp()
    
    elif "find my ip" in text or "ip address" in text:
        speak("Your IP address is " + find_my_ip())
    
    elif "what is the time" in text or "time" in text or "what time is" in text:
        what_is_the_time()
    
    elif "play music" in text or "play song" in text:
        speak("Okay, now starting...")

        # Check if a specific song name is mentioned
        song_name = text.replace("play music", "").replace("play song", "").strip()

        if song_name:  
            play_music(song_name)  # Play the specific song
        else:
            play_music()  # Play a random song
    
    elif "stop music" in text or "stop song" in text:
        speak("Stopping the music.")
        stop_music()  # Stops the music
    
    else:
        pass
