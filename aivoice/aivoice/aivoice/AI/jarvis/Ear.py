import speech_recognition as sr
import queue
import threading

class FastSpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_queue = queue.Queue()
        self.stop_listening = None
        self.recognized_text = None
        self.listening_active = threading.Event()

        # Optimized for Fast & Accurate Speech Detection
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.6  # Allow slightly longer pauses  
        self.recognizer.energy_threshold = 200  # Lower for better sensitivity  
        self.recognizer.non_speaking_duration = 0.3  # Reduce delay after speech

    def calibrate_noise(self):
        """Quick calibration for better accuracy."""
        with self.microphone as source:
            print("\n🔄 Calibrating microphone... Speak clearly after this.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Calibration complete. Listening now...")

    def start_listening(self):
        """Starts background listening and returns recognized speech."""
        self.listening_active.set()
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone,
            self.audio_callback,
            phrase_time_limit=4  # Limits speech capture to 4 sec
        )

        # Keep listening until speech is detected
        while self.listening_active.is_set():
            text = self.process_audio()
            if text:
                self.recognized_text = text
                break  # Stop listening once valid speech is detected

        self.cleanup()
        return self.recognized_text if self.recognized_text else ""  # Return empty string if nothing heard

    def audio_callback(self, recognizer, audio):
        """Receives audio and stores it for processing."""
        self.audio_queue.put(audio)

    def process_audio(self):
        """Processes first available audio input and converts it to text."""
        try:
            audio = self.audio_queue.get(timeout=2)  # Waits max 2 sec
            return self.recognize_speech(audio)
        except queue.Empty:
            return ""  # If no speech detected, return empty string

    def recognize_speech(self, audio):
        """Converts speech to text with error handling."""
        try:
            text = self.recognizer.recognize_google(audio, language="en-US").lower()
            print(f"\r🎤 You said: {text}", flush=True)
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"\n❌ API Error: {e}")
            return ""

    def cleanup(self):
        """Stops listening and releases resources."""
        self.listening_active.clear()
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        print("\n⏹️ Stopped listening.")

def listen():
    asr = FastSpeechRecognizer()
    asr.calibrate_noise()
    return asr.start_listening()  # Returns the first detected phrase