import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import datetime

# Initialize recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

# Create folder for saving wav files
if not os.path.exists("recordings"):
    os.makedirs("recordings")

print("🎙️ Real-time English → Hindi Speech-to-Speech Started...")

while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            # Step 1: Speech → Text (English)
            english_text = recognizer.recognize_google(audio, language="en-IN")
            print(f"📝 English: {english_text}")

            # Step 2: Translate to Hindi
            hindi_text = translator.translate(english_text, src="en", dest="hi").text
            print(f"🌐 Hindi: {hindi_text}")

            # Step 3: Hindi Text → Speech
            tts = gTTS(hindi_text, lang="hi")
            filename = f"recordings/output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            tts.save(filename)
            print(f"💾 Saved: {filename}")

    except sr.UnknownValueError:
        print("⚠️ Could not understand, skipping...")
    except KeyboardInterrupt:
        print("🛑 Stopped by user")
        break
