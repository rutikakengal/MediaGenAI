import os
import glob
import datetime
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment

# ---------- Config ----------
RAW_ENGLISH = "raw_data/english"
RAW_HINDI = "raw_data/hindhi"
DATASET_DIR = "dataset"

recognizer = sr.Recognizer()

os.makedirs(DATASET_DIR, exist_ok=True)

def ensure_dirs(direction):
    base = os.path.join(DATASET_DIR, direction)
    for sub in ["original_audio", "original_text", "translated_text", "translated_audio"]:
        os.makedirs(os.path.join(base, sub), exist_ok=True)
    return base

def split_text(text, max_length=4500):
    """Split text into chunks within GoogleTranslator's 5000 char limit."""
    chunks = []
    while len(text) > max_length:
        split_point = text.rfind(" ", 0, max_length)
        if split_point == -1:
            split_point = max_length
        chunks.append(text[:split_point])
        text = text[split_point:]
    chunks.append(text)
    return chunks

def process_file(file_path, direction):
    base = ensure_dirs(direction)

    if direction == "en2hi":
        lang_src_stt = "en-IN"   # Speech Recognition language
        lang_src_code = "en"     # Translator language code
        lang_dest_code = "hi"
    else:  # hi2en
        lang_src_stt = "hi-IN"
        lang_src_code = "hi"
        lang_dest_code = "en"

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.splitext(os.path.basename(file_path))[0]

    # Convert everything to WAV
    wav_path = os.path.join(base, "original_audio", f"{filename}_{ts}.wav")
    try:
        if file_path.lower().endswith(".mp3"):
            sound = AudioSegment.from_mp3(file_path)
            sound.export(wav_path, format="wav")
        elif file_path.lower().endswith(".wav"):
            sound = AudioSegment.from_wav(file_path)
            sound.export(wav_path, format="wav")
        else:
            print(f"⚠️ Skipped unsupported file: {file_path}")
            return
    except Exception as e:
        print(f"⚠️ Failed to convert {file_path} to WAV: {e}")
        return

    # Speech-to-text
    original_text = ""
    try:
        with sr.AudioFile(wav_path) as source:
            while True:
                audio_data = recognizer.record(source, duration=30)  # 30s chunks
                if not audio_data.frame_data:
                    break
                try:
                    text_chunk = recognizer.recognize_google(audio_data, language=lang_src_stt)
                    original_text += " " + text_chunk
                except sr.UnknownValueError:
                    continue
    except Exception as e:
        print(f"⚠️ Could not process audio {file_path}: {e}")
        return

    if not original_text.strip():
        print(f"⚠️ Could not transcribe {file_path}")
        return

    # Save original text
    with open(os.path.join(base, "original_text", f"{filename}_{ts}.txt"), "w", encoding="utf-8") as f:
        f.write(original_text.strip())

    # Translate in safe chunks
    translated_text = ""
    try:
        for chunk in split_text(original_text.strip()):
            translated_text += " " + GoogleTranslator(source=lang_src_code, target=lang_dest_code).translate(chunk)
    except Exception as e:
        print(f"⚠️ Translation failed for {file_path}: {e}")
        return

    # Save translated text
    with open(os.path.join(base, "translated_text", f"{filename}_{ts}.txt"), "w", encoding="utf-8") as f:
        f.write(translated_text.strip())

    # TTS of translated text
    tts_out = os.path.join(base, "translated_audio", f"{filename}_{ts}.mp3")
    try:
        gTTS(text=translated_text, lang=lang_dest_code).save(tts_out)
    except Exception as e:
        print(f"⚠️ TTS failed for {file_path}: {e}")
        return

    print(f"✅ Processed {file_path} -> {direction} dataset")

def build_dataset():
    # English → Hindi
    for f in glob.glob(os.path.join(RAW_ENGLISH, "*.mp3")) + glob.glob(os.path.join(RAW_ENGLISH, "*.wav")):
        process_file(f, "en2hi")

    # Hindi → English
    for f in glob.glob(os.path.join(RAW_HINDI, "*.mp3")) + glob.glob(os.path.join(RAW_HINDI, "*.wav")):
        process_file(f, "hi2en")

if __name__ == "__main__":
    build_dataset()
