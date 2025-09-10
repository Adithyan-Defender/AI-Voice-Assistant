import webbrowser
import difflib
import random
from DLG import websites, open_dld, success_open, open_maybe, sorry_open
from Mouth import speak

def openweb(text):
    """Opens a website using webbrowser while handling typos and errors."""
    if isinstance(text, list):
        text = " ".join(text)  # Combine list items into a single string

    website_name_lower = text.lower().strip()
    speak(f"Searching for: {website_name_lower}")  # Debugging log

    if website_name_lower in websites:
        url = websites[website_name_lower]
        speak(random.choice(open_dld) + f" {text}")
        webbrowser.open(url)  # ✅ Opens URL using the default browser

    else:
        # Find closest match (helps with typos)
        matches = difflib.get_close_matches(website_name_lower, websites.keys(), n=1, cutoff=0.6)
        if matches:
            closest_match = matches[0]
            url = websites[closest_match]
            speak(f"⚠️ Did you mean: {closest_match}? Opening {url}")
            speak(random.choice(open_maybe) + f" {text}, opening {closest_match} instead.")
            webbrowser.open(url)  # ✅ Opens closest-matching website
        else:
            speak(f"❌ No match found for: {text}")
            speak(random.choice(sorry_open) + f" I couldn't find {text}.")
