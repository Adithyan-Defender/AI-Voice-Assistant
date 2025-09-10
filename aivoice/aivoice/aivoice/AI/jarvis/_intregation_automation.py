from common_intregation import *
from google_intregation_main import *
from battery_intregation_main import *
from youtube_intregation_main import *




def Automation(text):
    youtube_cmd(text)
    google_cmd(text)
    battery_cmd(text)
    common_cmd(text)

