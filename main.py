import os
import subprocess
import webbrowser as wb
import datetime
import pyautogui
import psutil
import keyboard
import platform
import threading
import speech_recognition as sr
from gtts import gTTS
import pygame
from decouple import config
from plyer import notification

# ---------- OS Detection ----------
OS_NAME = platform.system()  # 'Windows' or 'Darwin' (Mac)
if OS_NAME == "Windows":
    import win32gui
    import win32con
    import win32api

pygame.mixer.init()
recognizer = sr.Recognizer()

import google.generativeai as genai
GOOGLE_KEY = config("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
memory = []

def speak(text):
    try:
        tts = gTTS(text)
        tts.save("voice.mp3")
        pygame.mixer.music.load("voice.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove("voice.mp3")
    except Exception as e:
        print("TTS Error:", e)

def ai(text):
    memory.append(text)
    try:
        response = model.generate_content("\n".join(memory[-8:]))
        reply = response.text
    except Exception as e:
        reply = "Sorry, I couldn't process that."
        print("AI Error:", e)
    memory.append(reply)
    speak(reply)

def show_notification(msg):
    notification.notify(title="Iris", message=msg, timeout=4)

def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    if OS_NAME == "Windows":
        img = pyautogui.screenshot()
        img.save(filename)
    elif OS_NAME == "Darwin":
        os.system(f"screencapture -x {filename}")
    speak(f"Screenshot saved as {filename}")

def control_volume(action):
    if OS_NAME == "Windows":
        if "up" in action:
            for _ in range(5): win32api.keybd_event(0xAF, 0, 0, 0)
        elif "down" in action:
            for _ in range(5): win32api.keybd_event(0xAE, 0, 0, 0)
        elif "mute" in action:
            win32api.keybd_event(0xAD, 0, 0, 0)
    elif OS_NAME == "Darwin":
        if "up" in action:
            os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
        elif "down" in action:
            os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
        elif "mute" in action:
            os.system("osascript -e 'set volume output muted not (output muted of (get volume settings))'")
    speak("Done")

def window_action(action):
    if OS_NAME == "Windows":
        hwnd = win32gui.GetForegroundWindow()
        if "minimize" in action:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        elif "maximize" in action:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        elif "close" in action:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    elif OS_NAME == "Darwin":
        script = ""
        if "minimize" in action:
            script = 'tell application "System Events" to set miniaturized of windows of (first application process whose frontmost is true) to true'
        elif "maximize" in action:
            script = 'tell application "System Events" to set bounds of front window of (first application process whose frontmost is true) to {0, 0, 1440, 900}'
        elif "close" in action:
            script = 'tell application "System Events" to keystroke "w" using {command down}'
        if script:
            os.system(f"osascript -e '{script}'")
    speak("Done")

def open_any_app(name):
    name = name.lower().strip()
    if OS_NAME == "Windows":
        fuzzy_apps = {
            "notepad": ["notepad", "note pad", "editor", "text editor"],
            "cmd": ["cmd", "command prompt", "terminal", "console"],
            "calculator": ["calculator", "calc"],
            "paint": ["paint", "mspaint"],
            "task manager": ["task manager", "tasks"]
        }
        for app_key, keywords in fuzzy_apps.items():
            if any(k in name for k in keywords):
                exe_name = {
                    "notepad": "notepad.exe",
                    "cmd": "cmd.exe",
                    "calculator": "calc.exe",
                    "paint": "mspaint.exe",
                    "task manager": "taskmgr.exe"
                }[app_key]
                try:
                    if app_key == "cmd":
                        subprocess.Popen(["cmd", "/c", "start", "cmd"], shell=True)
                    else:
                        subprocess.Popen(exe_name, shell=True)
                    speak(f"Opening {app_key}")
                    return
                except Exception as e:
                    speak(f"Cannot open {app_key}")
                    print("Open app error:", e)
                    return
    elif OS_NAME == "Darwin":
        fuzzy_apps = {
            "textedit": ["textedit", "editor", "notepad"],
            "terminal": ["terminal", "cmd", "console", "command prompt"],
            "calculator": ["calculator", "calc"],
            "preview": ["preview", "paint"],
            "activity monitor": ["task manager", "activity monitor", "tasks"]
        }
        for app_key, keywords in fuzzy_apps.items():
            if any(k in name for k in keywords):
                app_map = {
                    "textedit": "TextEdit",
                    "terminal": "Terminal",
                    "calculator": "Calculator",
                    "preview": "Preview",
                    "activity monitor": "Activity Monitor"
                }
                try:
                    subprocess.Popen(["open", "-a", app_map[app_key]])
                    speak(f"Opening {app_key}")
                    return
                except Exception as e:
                    speak(f"Cannot open {app_key}")
                    print("Open app error:", e)
                    return
    speak("Application not found")

def search_file(name):
    speak("Searching file")
    if OS_NAME == "Windows":
        for root, dirs, files in os.walk("C:\\"):
            for f in files:
                if name.lower() in f.lower():
                    os.startfile(os.path.join(root, f))
                    speak("File opened")
                    return
    elif OS_NAME == "Darwin":
        os.system(f"mdfind '{name}' | head -n 1 | xargs open -R")
    speak("File not found")

def get_system_status():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    speak(f"CPU at {cpu} percent and RAM at {ram} percent")

def process(cmd):
    cmd = cmd.lower()
    if "time" in cmd:
        speak(datetime.datetime.now().strftime("%I:%M %p"))
    elif "date" in cmd:
        speak(datetime.date.today().strftime("%A %d %B %Y"))
    elif "volume" in cmd:
        control_volume(cmd)
    elif "screenshot" in cmd:
        take_screenshot()
    elif "status" in cmd or "system" in cmd:
        get_system_status()
    elif "minimize" in cmd or "maximize" in cmd or "close window" in cmd:
        window_action(cmd)
    elif "open" in cmd:
        app = cmd.replace("open", "").strip()
        open_any_app(app)
    elif "file" in cmd:
        name = cmd.replace("file", "").strip()
        search_file(name)
    elif "notification" in cmd:
        show_notification("Hello from Iris")
        speak("Notification sent")
    elif "browser" in cmd:
        wb.open("https://google.com")
        speak("Opening browser")
    elif "shutdown" in cmd:
        speak("Shutting down")
        if OS_NAME == "Windows":
            os.system("shutdown /s /t 1")
        elif OS_NAME == "Darwin":
            os.system("osascript -e 'tell app \"System Events\" to shut down'")
    elif "restart" in cmd:
        speak("Restarting")
        if OS_NAME == "Windows":
            os.system("shutdown /r /t 1")
        elif OS_NAME == "Darwin":
            os.system("osascript -e 'tell app \"System Events\" to restart'")
    elif "exit" in cmd or "close iris" in cmd:
        speak("Goodbye")
        exit()
    else:
        ai(cmd)

def wake_word_listener():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=3)
                text = recognizer.recognize_google(audio, language="en-IN").lower()
                if "iris" in text:
                    speak("Yes?")
                    listen_for_command()
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print("Wake word error:", e)

def listen_for_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, phrase_time_limit=5)
            try:
                text = recognizer.recognize_google(audio, language="en-IN")
            except:
                text = recognizer.recognize_google(audio, language="hi-IN")
            print("Command:", text)
            process(text)
        except Exception as e:
            speak("Say that again please")
            print("Command error:", e)

def hotkey_listener():
    while True:
        keyboard.wait("ctrl+alt+i")
        speak("Listening")
        listen_for_command()

# ---------- MAIN ----------
if __name__ == "__main__":
    speak("Iris ready for voice activation")
    threading.Thread(target=wake_word_listener, daemon=True).start()
    hotkey_listener()
