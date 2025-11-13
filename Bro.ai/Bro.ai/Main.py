import os
import sys
import asyncio
import webview
import json
import re
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_PATH = os.path.join(BASE_DIR, "Backend")
sys.path.append(BACKEND_PATH)

from Backend.SpeechToText import get_translated_text, mic_status
from Model import QueryClassifier
from Chatbot import chat_with_Bro_ai
from RealtimeSearchEngine import realtime_answer
from ImageGeneration import generate_image
from TextToSpeech import speak, shutdown_tts
from GUI import create_webview_window
from Automation import (
    open_app, close_app,
    mute_volume, volume_up, volume_down,
    restart_pc, shutdown_pc, refresh_pc,
    toggle_bluetooth, toggle_airplane_mode,
    play_youtube, play_spotify,
    write_content
)

classifier = QueryClassifier()
speak_futures = []
query_queue = []

def save_message(role, content):
    chat_path = r"[ENTER YOUR SAFE CHAT.JSON PATH HERE]"
    try:
        with open(chat_path, "r", encoding="utf-8") as f:
            chat_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        chat_data = []

    chat_data.append({"role": role, "content": content})
    with open(chat_path, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=2, ensure_ascii=False)

def track_speak(future):
    if future and not future.cancelled():
        speak_futures.append(future)

class QueryAPI:
    def submit_query(self, query):
        if query and query.strip():
            query_queue.append(query.strip())
            print(f" Query received from frontend: {query}")
            return {"status": "success", "message": "Query received"}
        return {"status": "error", "message": "Empty query"}
    
    def get_query_status(self):
        return {"queue_length": len(query_queue), "status": "ready"}
    
    def clear_chat(self):
        chat_path = r"[ENTER YOUR SAFE CHAT.JSON PATH HERE]"
        try:
            with open(chat_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2, ensure_ascii=False)
            print(" Chat history cleared successfully")
            return {"status": "success", "message": "Chat cleared"}
        except Exception as e:
            print(f" Error clearing chat: {e}")
            return {"status": "error", "message": str(e)}

async def handle_task(task_type, specific_query):
    task_type = task_type.lower()
    is_control_task = False

    try:
        if task_type.startswith("chat") or task_type.startswith("general"):
            reply = chat_with_Bro_ai(specific_query)
            print(" Bro_ai:", reply)
            save_message("assistant", reply)
            f = speak(reply)
            track_speak(f)

        elif task_type.startswith("google search"):
            topic = task_type.replace("google search", "").strip()
            os.system(f'start https://www.google.com/search?q={topic.replace(" ", "+")}')
            f = speak(f"Searching Google for {topic}")
            track_speak(f)
            is_control_task = True

        elif task_type.startswith("youtube search"):
            topic = task_type.replace("youtube search", "").strip()
            os.system(f'start https://www.youtube.com/results?search_query={topic.replace(" ", "+")}')
            f = speak(f"Searching YouTube for {topic}")
            track_speak(f)
            is_control_task = True

        elif task_type.startswith("spotify search"):
            topic = task_type.replace("spotify search", "").strip()
            os.system(f'start https://open.spotify.com/search/{topic.replace(" ", "%20")}')
            f = speak(f"Searching Spotify for {topic}")
            track_speak(f)
            is_control_task = True

        elif task_type.startswith("realtime") or task_type.startswith("search"):
            reply = realtime_answer(specific_query)
            print(" Bro_ai:", reply)
            save_message("assistant", reply)
            f = speak(reply)
            track_speak(f)

        elif task_type.startswith("generate") or task_type.startswith("image"):
            await generate_image(specific_query)
            is_control_task = True

        elif task_type.startswith("open "):
            app = task_type.replace("open", "").strip()
            await asyncio.to_thread(open_app, app)
            is_control_task = True

        elif task_type.startswith("close "):
            app = task_type.replace("close", "").strip()
            await asyncio.to_thread(close_app, app)
            is_control_task = True

        elif "mute" in task_type:
            mute_volume()
            is_control_task = True
        elif "volume up" in task_type:
            volume_up()
            is_control_task = True
        elif "volume down" in task_type:
            volume_down()
            is_control_task = True
        elif "restart" in task_type:
            restart_pc()
            is_control_task = True
        elif "shutdown" in task_type:
            shutdown_pc()
            is_control_task = True
        elif "refresh" in task_type:
            refresh_pc()
            is_control_task = True
        elif "bluetooth on" in task_type:
            toggle_bluetooth(True)
            is_control_task = True
        elif "bluetooth off" in task_type:
            toggle_bluetooth(False)
            is_control_task = True
        elif "airplane mode on" in task_type:
            toggle_airplane_mode(True)
            is_control_task = True
        elif "airplane mode off" in task_type:
            toggle_airplane_mode(False)
            is_control_task = True
        elif "wifi on" in task_type:
            await asyncio.to_thread(open_app, "wifi")
            is_control_task = True
        elif "wifi off" in task_type:
            await asyncio.to_thread(close_app, "wifi")
            is_control_task = True

        elif task_type.startswith("play"):
            song = task_type.replace("play", "").strip()
            if "spotify" in task_type:
                cleaned = re.sub(r"\b(play|spotify|on|music|audio)\b", "", song).strip()
                await play_spotify(cleaned)
            else:
                await play_youtube(song)
            is_control_task = True

        elif task_type.startswith("content"):
            await write_content(specific_query)
            is_control_task = True

        else:
            print(" Unknown task:", task_type)
            return

        if is_control_task:
            confirm = "Done sir, let me know anything needed."
            print(" Bro_ai:", confirm)
            save_message("assistant", confirm)
            f = speak(confirm)
            track_speak(f)

    except Exception as e:
        print(f" Error in task '{task_type}': {e}")

async def main_loop():
    print("\n Bro_ai is ready. Use the frontend 'Ask Anything' box to submit queries.\n")
    while True:
        if query_queue:
            query = query_queue.pop(0)
            print(f" Processing query: {query}")
            save_message("user", query)
            task_list = classifier.classify(query)
            await asyncio.gather(*[
                handle_task(task_type=task, specific_query=query)
                for task in task_list
            ])
        
        if mic_status.get("on", False):
            try:
                speech_query = get_translated_text()
                if speech_query:
                    print(f" Speech detected: {speech_query}")
                    save_message("user", speech_query)
                    task_list = classifier.classify(speech_query)
                    await asyncio.gather(*[
                        handle_task(task_type=task, specific_query=speech_query)
                        for task in task_list
                    ])
            except Exception as e:
                print(f" Speech recognition error: {e}")
        
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    def start_Bro_ai():
        try:
            intro = (
                "Hey Bro!, I'm your personal AI assistant. you can call me Bro.ai"
            )
            
            save_message("assistant", intro)
            f = speak(intro)
            track_speak(f)

            asyncio.run(main_loop())
        finally:
            print("\n Waiting for TTS to complete...")
            for future in speak_futures:
                try:
                    future.result(timeout=10)
                except Exception:
                    pass
            shutdown_tts()
            print("Bro_ai shut down gracefully.")

    window = create_webview_window(QueryAPI())
    webview.start(func=start_Bro_ai, gui='edgechromium', debug=False)
