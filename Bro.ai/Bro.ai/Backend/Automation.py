import asyncio
import os
import webbrowser
import pyautogui
import subprocess
import pywhatkit
import time
import psutil
from groq import Groq
from dotenv import load_dotenv
import difflib
from googlesearch import search

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
USER_NAME = os.getenv("USER_NAME", "User")
BOT_NAME = os.getenv("BOT_NAME", "Bro.ai")

client = Groq(api_key=GROQ_API_KEY)

def mute_volume():
    pyautogui.press("volumemute")

def volume_up():
    for _ in range(5):
        pyautogui.press("volumeup")

def volume_down():
    for _ in range(5):
        pyautogui.press("volumedown")

def restart_pc():
    print("Restarting PC...")
    os.system("shutdown /r /t 1")

def shutdown_pc():
    print("Shutting down PC...")
    os.system("shutdown /s /t 1")

def refresh_pc():
    pyautogui.hotkey("f5")

def toggle_bluetooth(on=True):
    pyautogui.hotkey("win", "a")
    time.sleep(1)
    pyautogui.moveTo(1800, 500)
    pyautogui.click()
    pyautogui.hotkey("win", "a")

def toggle_airplane_mode(on=True):
    pyautogui.hotkey("win", "a")
    time.sleep(1)
    pyautogui.moveTo(1800, 600)
    pyautogui.click()
    pyautogui.hotkey("win", "a")


def open_whatsapp():
    try:
        subprocess.Popen('explorer shell:AppsFolder\[enter the app link]')
        print("WhatsApp launched!")
        return True
    except Exception as e:
        print(f"Error launching WhatsApp: {e}")
        return False

def open_spotify():
    spotify_path = os.path.expandvars(r"[enter the app folder path]")
    if os.path.exists(spotify_path):
        try:
            subprocess.Popen([spotify_path])
            print("Spotify launched!")
            return True
        except Exception as e:
            print(f"Error launching Spotify: {e}")
            return False
    else:
        print("Spotify.exe not found.")
        return False

def open_adobe_acrobat():
    acrobat_path = r"[enter your acrobat path]"
    if os.path.exists(acrobat_path):
        try:
            subprocess.Popen([acrobat_path])
            print("Adobe Acrobat launched!")
            return True
        except Exception as e:
            print(f"Error launching Acrobat: {e}")
            return False
    else:
        print("Adobe Acrobat.exe not found.")
        return False

def open_word():
    possible_paths = [
        os.path.expandvars(r"[enter your word path]"),
        os.path.expandvars(r"[enter your word path]"),
        os.path.expandvars(r"[enter your word path]"),
        os.path.expandvars(r"[enter your word path]")
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                subprocess.Popen([path])
                print("Microsoft Word launched!")
                return True
            except Exception as e:
                print(f"Error launching Word: {e}")
                return False
    print("Microsoft Word executable not found.")
    return False

def open_camera():
    try:
        subprocess.Popen("start microsoft.windows.camera:", shell=True)
        print("Camera launched!")
        return True
    except Exception as e:
        print(f"Error launching Camera: {e}")
        return False


def open_app(app_name):
    app_name = app_name.lower().strip()
    supported_apps = {
        "whatsapp": open_whatsapp,
        "spotify": open_spotify,
        "adobe": open_adobe_acrobat,
        "word": open_word,
        "notepad": lambda: subprocess.Popen(["notepad.exe"]) or print("Notepad launched!") or True,
        "calculator": lambda: subprocess.Popen(["calc.exe"]) or print("Calculator launched!") or True,
        "excel": lambda: subprocess.Popen(["EXCEL.EXE"]) or print("Excel launched!") or True,
        "camera": open_camera,
    }
    close_matches = difflib.get_close_matches(app_name, supported_apps.keys(), n=1, cutoff=0.6)
    matched_app = close_matches[0] if close_matches else None

    if matched_app:
        success = supported_apps[matched_app]()
        if not success:
            print(f" Failed to launch {matched_app} locally. Searching on Google...")
            try:
                for url in search(f"{matched_app} official site", num_results=1):
                    print(f" Opening: {url}")
                    webbrowser.open(url)
                    break
            except Exception as e:
                print(f" Google search failed: {e}")
    else:
        print(f" '{app_name}' not recognized locally. Searching on Google...")
        try:
            for url in search(f"{app_name} official site", num_results=1):
                print(f" Opening: {url}")
                webbrowser.open(url)
                break
        except Exception as e:
            print(f" Google search failed: {e}")


def close_app(app_name):
    process_name_map = {
        "whatsapp": ["WhatsApp.exe"],
        "spotify": ["Spotify.exe"],
        "word": ["WINWORD.EXE", "winword.exe"],
        "adobe": ["Acrobat.exe"],
        "notepad": ["notepad.exe"],
        "calculator": ["Calculator.exe", "calc.exe"],
        "excel": ["EXCEL.EXE", "excel.exe"],
    }
    process_names = process_name_map.get(app_name.lower(), [app_name])
    closed_any = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and any(pname.lower() == proc.info['name'].lower() for pname in process_names):
                print(f"Closing {proc.info['name']} (PID {proc.info['pid']})")
                proc.terminate()
                proc.wait(timeout=5)
                closed_any = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    if closed_any:
        print(f"{app_name.capitalize()} closed.")
    else:
        print(f"No running app found with name: {app_name}")


async def search_google(topic):
    print(f"Searching Google for: {topic}")
    pywhatkit.search(topic)

async def write_content(topic, filename="generated_content.txt"):
    print(f"Generating content for: {topic} ...")

    skip_words = ["open", "launch", "start", "whatsapp", "instagram", "youtube", "google", "spotify", "app"]
    words = topic.split()
    cleaned_words = [w for w in words if w.lower() not in skip_words]
    cleaned_topic = " ".join(cleaned_words).strip()
    if not cleaned_topic:
        cleaned_topic = topic.strip()

    messages = [
        {"role": "system", "content": f"You are {BOT_NAME}, a helpful assistant for {USER_NAME}."},
        {"role": "user", "content": f"Write a short letter or note about the following topic, without giving instructions or tool usage: {cleaned_topic}"}
    ]
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )
    content = response.choices[0].message.content

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f" Content saved to {filename}")
    os.startfile(filename)

async def play_youtube(topic):
    print(f"Playing on YouTube: {topic}")
    pywhatkit.playonyt(topic)

async def play_spotify(song):
    print(f"Playing on Spotify: {song}")
    spotify_path = os.path.expandvars(r"[enter the app folder path]")
    try:
        if os.path.exists(spotify_path):
            subprocess.Popen([spotify_path])
            print("Launched Spotify desktop app.")
            time.sleep(7)
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(1)
            pyautogui.typewrite(song)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(3)
            pyautogui.moveTo(450, 350)
            pyautogui.click()
            time.sleep(1.5)
            scroll_keywords = ["lofi", "sad song", "top 10", "top100", "top 100", "many", "relaxing", "mood", "beats", "romantic", "study", "rain", "instrumental"]
            if any(keyword in song.lower() for keyword in scroll_keywords):
                pyautogui.scroll(-116)
                time.sleep(1)
                pyautogui.moveTo(450, 500)
                pyautogui.click()
                time.sleep(0.5)
                pyautogui.press("enter")
            else:
                pyautogui.press("enter")
            time.sleep(1)
        else:
            print("Spotify.exe not found. Opening in browser...")
            webbrowser.open(f"https://open.spotify.com/search/{song}")
    except Exception:
        webbrowser.open(f"https://open.spotify.com/search/{song}")

async def handle_tasks(commands):
    tasks = []
    for command in commands:
        cmd = command.lower()
        if cmd.startswith("search google"):
            topic = cmd.replace("search google", "").strip()
            tasks.append(search_google(topic))
        elif cmd.startswith("write content"):
            topic = cmd.replace("write content", "").strip()
            tasks.append(write_content(topic))
        elif cmd.startswith("content "):
            topic = cmd.replace("content", "").strip()
            tasks.append(write_content(topic))
        elif cmd.startswith("play youtube"):
            topic = cmd.replace("play youtube", "").strip()
            tasks.append(play_youtube(topic))
        elif cmd.startswith("play spotify"):
            song = cmd.replace("play spotify", "").strip()
            tasks.append(play_spotify(song))
        elif cmd.startswith("play") and "on spotify" in cmd:
            song = cmd.replace("play", "").replace("on spotify", "").strip()
            tasks.append(play_spotify(song))
        elif cmd.startswith("open app"):
            app_name = cmd.replace("open app", "").strip()
            tasks.append(asyncio.to_thread(open_app, app_name))
        elif cmd.startswith("open "):
            if not cmd.startswith("open app"):
                app_name = cmd.replace("open", "").strip()
                tasks.append(asyncio.to_thread(open_app, app_name))
        elif cmd.startswith("close app"):
            app_name = cmd.replace("close app", "").strip()
            tasks.append(asyncio.to_thread(close_app, app_name))
        elif cmd.startswith("close "):
            app_name = cmd.replace("close", "").strip()
            tasks.append(asyncio.to_thread(close_app, app_name))
        elif "mute" == cmd:
            tasks.append(asyncio.to_thread(mute_volume))
        elif "volume up" == cmd:
            tasks.append(asyncio.to_thread(volume_up))
        elif "volume down" == cmd:
            tasks.append(asyncio.to_thread(volume_down))
        elif "restart pc" == cmd:
            tasks.append(asyncio.to_thread(restart_pc))
        elif "shutdown pc" == cmd:
            tasks.append(asyncio.to_thread(shutdown_pc))
        elif "refresh pc" == cmd:
            tasks.append(asyncio.to_thread(refresh_pc))
        elif "bluetooth on" == cmd:
            tasks.append(asyncio.to_thread(toggle_bluetooth, True))
        elif "bluetooth off" == cmd:
            tasks.append(asyncio.to_thread(toggle_bluetooth, False))
        elif "airplane mode on" == cmd:
            tasks.append(asyncio.to_thread(toggle_airplane_mode, True))
        elif "airplane mode off" == cmd:
            tasks.append(asyncio.to_thread(toggle_airplane_mode, False))
        else:
            print(f"Command not recognized or supported: '{cmd}'")
    if tasks:
        await asyncio.gather(*tasks)
    print(" All tasks completed.")

def split_commands(user_input: str):
    if not user_input.strip():
        return []
    parts = []
    for chunk in user_input.split(";"):
        sub_parts = chunk.split(" and ")
        parts.extend([p.strip() for p in sub_parts if p.strip()])
    return parts

if __name__ == "__main__":
    print(f">>> Hello {USER_NAME}! Type commands separated by ';' or single command.")
    while True:
        try:
            print(">>> ", end="", flush=True)
            user_input = input().strip()
            if not user_input:
                continue
            commands = split_commands(user_input)
            asyncio.run(handle_tasks(commands))
        except KeyboardInterrupt:
            print("\nExiting...")
            break