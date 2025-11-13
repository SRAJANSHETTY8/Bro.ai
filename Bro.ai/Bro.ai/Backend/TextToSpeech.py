import asyncio
import tempfile
import os
import random
import threading
import sounddevice as sd
import soundfile as sf
from edge_tts import Communicate
import re
import sys
import contextlib
import io

VOICE = "en-GB-RyanNeural"

PHRASES = [
    "Take a look at this, sir.",
    "Please have a look at this.",
    "Let me know if you need anything else.",
    "Hope that helps.",
    "That's what I found.",
    "Here's what I gathered for you.",
    "That's something you might find useful.",
    "Let me explain that to you.",
    "That’s all I could summarize for now.",
    "Let me know if you want me to go deeper."
]

def get_two_and_half_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(sentences) <= 3:
        return " ".join(sentences), False

    selected = sentences[:3]
    third_sentence = sentences[3]
    words = third_sentence.split()
    if len(words) <= 3:
        selected.append(third_sentence)
    else:
        partial_words = []
        word_count = 0
        for w in words:
            partial_words.append(w)
            word_count += 1
            if w.endswith('.') and word_count >= 3:
                break
        partial_sentence = " ".join(partial_words)
        selected.append(partial_sentence)

    line_count = len([s for s in sentences if s.strip()])
    return " ".join(selected), line_count >=5

async def generate_and_play(text: str):
    try:
        clean_text = text.strip()
        if not clean_text:
            print("[TTS] Skipping empty text.")
            return

        selected_text, should_add_phrase = get_two_and_half_sentences(clean_text)
        if should_add_phrase:
            phrase = random.choice(PHRASES)
            final_text = f"{selected_text} {phrase}"
        else:
            final_text = selected_text

        ssml_text = final_text
        print(f"Bro.ai: {ssml_text}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            filename = tmpfile.name

        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            communicate = Communicate(ssml_text, voice=VOICE)
            await communicate.save(filename)

        data, fs = sf.read(filename, dtype='float32')
        sd.play(data, fs)
        sd.wait()
        os.remove(filename)

    except Exception as e:
        print(f"[TTS ERROR] generate_and_play(): {e}")

class TTSManager:
    def __init__(self):
        self.loop = None
        self.thread = None
        self.running = False
        self.lock = threading.Lock()
        print("SYSTEM INITIALIZED")
        self._start_loop()

    def _start_loop(self):
        with self.lock:
            if self.running:
                print("")
                return
            print("CHECKING SYSTEM FUCTIONS.")
            self.loop = asyncio.new_event_loop()
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.running = True
            self.thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        try:
            print("SYSTEM CHECKS ALL CLEAR")
            self.loop.run_forever()
        except Exception as e:
            print(f"[TTS ERROR] Event loop crashed: {e}")
        finally:
            print("[TTS] Event loop terminated.")
            self.running = False

    def speak(self, text):
        with self.lock:
            if not self.running:
                print("[TTS]  speak(): Loop not running.")
                return None
            if not self.loop:
                print("[TTS]  speak(): Loop is None.")
                return None
            if not self.loop.is_running():
                print("[TTS]  speak(): Loop is not running.")
                return None
            if sys.is_finalizing():
                print("[TTS]  speak(): Python interpreter is shutting down.")
                return None

            try:
                print("")
                future = asyncio.run_coroutine_threadsafe(generate_and_play(text), self.loop)
                return future
            except Exception as e:
                print(f"[TTS ERROR] speak(): {e}")
                return None

    def stop_loop(self):
        with self.lock:
            if self.running and self.loop and self.loop.is_running():
                print("[TTS] Stopping event loop...")
                self.loop.call_soon_threadsafe(self.loop.stop)
                self.thread.join()
                print("[TTS] Thread joined successfully.")
            else:
                print("[TTS] Loop already stopped or was never started.")
            self.running = False
            self.loop = None
            self.thread = None
            print("[TTS] Loop cleanup complete.")

tts_manager = TTSManager()

def speak(text: str):
    return tts_manager.speak(text)

def shutdown_tts():
    print("[TTS] Shutdown initiated...")
    tts_manager.stop_loop()

if __name__ == "__main__":
    print("Enter text to speak (Ctrl+C to exit):")
    try:
        while True:
            inp = input(">>> ").strip()
            if not inp:
                continue
            speak(inp)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        shutdown_tts()