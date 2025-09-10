import random
import time
import pyautogui as ui
import webbrowser
from DLG import yt_search, s1, s2
from Mouth import speak

def youtube_search(text):
    dlg = random.choice(yt_search)
    speak(dlg)
    
    # Open YouTube in the browser
    webbrowser.open("https://www.youtube.com/")
    
    time.sleep(4)  # Wait for the page to fully load
    
    # Press "Tab" multiple times to focus the search bar
    for _ in range(4):  # Adjust the number of tabs based on browser behavior
        ui.press("tab")
        time.sleep(0.3)  # Small delay between presses
    
    # Type the search query and press Enter
    ui.write(text)
    s12 = random.choice(s1)
    speak(s12)
    time.sleep(0.5)
    ui.press("enter")
    
    s12 = random.choice(s2)
    speak(s12)


