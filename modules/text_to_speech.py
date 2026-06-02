id="v9kq1t"
import pyttsx3
import threading


def speak(text):

    if not text:
        return

    def run_speech():

        try:

            engine = pyttsx3.init()

            # ==========================================
            # VOICE SETTINGS
            # ==========================================

            voices = engine.getProperty("voices")

            # Select female voice if available
            if voices and len(voices) > 1:
                engine.setProperty("voice", voices[1].id)

            # Speed
            engine.setProperty("rate", 165)

            # Volume
            engine.setProperty("volume", 1.0)

            # ==========================================
            # CLEAN TEXT
            # ==========================================

            clean_text = str(text)

            clean_text = clean_text.replace("*", "")
            clean_text = clean_text.replace("#", "")
            clean_text = clean_text.replace("`", "")

            # ==========================================
            # SPEAK
            # ==========================================

            engine.say(clean_text)

            engine.runAndWait()

            engine.stop()

        except Exception as e:

            print("TTS ERROR:", e)

    # Run in separate thread
    threading.Thread(target=run_speech).start()

