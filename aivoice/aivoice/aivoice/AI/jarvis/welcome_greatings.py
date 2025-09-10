import random
from DLG import welcomedlg
from Mouth import speak


def welcome():
    welcome = random.choice(welcomedlg)
    speak(welcome)
