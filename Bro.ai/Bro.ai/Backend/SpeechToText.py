import os
import speech_recognition as sr
import requests
from dotenv import load_dotenv
import socket
from urllib.error import URLError, HTTPError
from langdetect import detect

try:
    from GUI import mic_status
except ImportError:
    mic_status = {"on": True}

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"

wh_words = ["what", "where", "when", "who", "whom", "whose", "why", "which", "how"]

def add_question_mark(text):
    words = text.lower().split()
    if any(word in words for word in wh_words):
        return text.rstrip(".!?") + "?"
    return text

def translate_with_groq(text_native):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Translate only the non-English (Indian language) parts of the sentence below to natural English. "
        f"Keep English words like app names (e.g., Spotify, YouTube), song titles (e.g., Adiye,channa mereya,ishq,khariyat), or commands (e.g., play, open) unchanged. "
        f"Do NOT explain meanings or define any word. Just return the complete translated sentence in fluent English:\n\n"
        f"{text_native}"
    )

    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print(" Groq API error:", response.text)
            return text_native
    except Exception as e:
        print(" Groq request failed:", e)
        return text_native

def fix_common_translation_errors(text):
    mapping = {
        "Whatsapp big": "Open WhatsApp",
        "Whatsapp kholo": "Open WhatsApp",
        "time kitna hua hai": "What time is it"
    }
    lower_text = text.lower()
    for wrong, correct in mapping.items():
        if wrong in lower_text:
            return correct
    return text

def recognize_and_translate():
    if not mic_status.get("on", True):
        print("[Mic Status] OFF - Skipping recognition.")
        return ""

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(" Speak something in any Indian language...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print(" Recognizing...")

            try:
                text_native = recognizer.recognize_google(audio)
            except (sr.RequestError, URLError, HTTPError, socket.error, ConnectionResetError) as e:
                print(f" Google recognition failed due to connection error: {e}")
                return ""

            print(f" You said: {text_native}")

            try:
                lang = detect(text_native)
                print(f" Detected language: {lang}")
            except Exception as e:
                print(" Language detection failed. Assuming unknown.")
                lang = "unknown"

            indian_langs = ["hi", "kn", "ta", "te", "ml", "gu", "mr", "bn", "pa", "or", "ur"]
            indian_keywords = [
                "mera", "tum", "kya", "kaise", "kyon", "batao", "kitna", "samay",
                "whatsapp", "kholo", "kar", "raha", "hai", "ho", "namaste", "bhai", "chal",
                "hesaru", "khana", "mein", "karna", "bana", "dost", "bapu", "maa", "baat",
                "majha", "naam", "spotify", "gana", "chalao", "per", "kaam", "kaam karo"
            ]

            words = text_native.lower().split()
            contains_indian_word = any(word in words for word in indian_keywords)
            is_short = len(text_native.split()) <= 4

            should_force_translate = (
                (lang in indian_langs or contains_indian_word) or
                (lang == "en" and contains_indian_word and is_short)
            )

            if lang == "en" and not contains_indian_word:
                print(f"Input is already English: {text_native}")
                translated = text_native
            elif should_force_translate:
                print(f" Treating as Indian language due to lang='{lang}', keyword match, or short phrase.")
                translated = translate_with_groq(text_native)
                print(f" Translated to English: {translated}")
            else:
                print(f" Input is already English or foreign language: {text_native}")
                translated = text_native

            translated = fix_common_translation_errors(translated)
            final_text = add_question_mark(translated)
            print(f" Final text: {final_text}")
            return final_text

        except sr.WaitTimeoutError:
            print(" Listening timed out.")
        except sr.UnknownValueError:
            print(" Could not understand the audio.")
        except Exception as e:
            print(f" Unexpected recognition error: {e}")
    return ""

def get_translated_text():
    return recognize_and_translate()

if __name__ == "__main__":
    final_text = recognize_and_translate()
    if final_text:
        print(f"\n Final Translated Text: {final_text}")
