import pywhatkit
import random
from DLG import search_result
from Mouth import speak


def search_google(text):
    dlg = random.choice(search_result)
    pywhatkit.search(text)
    speak(dlg)
