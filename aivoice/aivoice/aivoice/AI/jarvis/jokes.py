import random
import time

import requests



def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def jokes():
    while True:

        x = [600, 550, 580, 400, 3000, 800, 700, 8200 ,8000, 50 ,568]
        x = random.choice(x)
        time.sleep(x)
        print("I have some joke for you, sir")
        text = "yes".lower()
        if "yes tell me" in text or "yes" in text:
            advice = get_random_joke()
            print(advice)
            pass
        else:
            print("no problem sir, I just want to include some entertainment in your day ")
            pass

jokes()