# =====================================================
# IRIS DESKTOP ASSISTANT | PRO VERSION
# ShadowDev / code2encoder
# =====================================================

import os, json, time, queue, threading, subprocess, datetime, warnings, logging
import webbrowser as wb
import requests, psutil, keyboard, wmi
import speech_recognition as sr
from gtts import gTTS
import pygame
from decouple import config
import win32gui, win32con, win32api
import google.generativeai as genai

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
warnings.filterwarnings("ignore", category=FutureWarning)
logging.basicConfig(level=logging.ERROR)

# ---------------- INIT ----------------
pygame.mixer.init()
recognizer = sr.Recognizer()
tts_queue = queue.Queue()
silent_mode = False
last_wake = 0

genai.configure(api_key=config("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

memory = []

def show_banner():
    print("=" * 55)
    print("  This Iris Desktop Made By ShadowDev/code2encoder")
    print("=" * 55)

def get_city_coordinates(city):
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
    res = requests.get(url, headers={"User-Agent": "Iris"}).json()
    if not res:
        return None, None
    return float(res[0]["lat"]), float(res[0]["lon"])


def listen_city():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        speak("Which city?")
        audio = recognizer.listen(source, phrase_time_limit=4)
        city = recognizer.recognize_google(audio, language="en-IN")
        print("City:", city)
        return city


def get_weather_city(city):
    try:
        lat, lon = get_city_coordinates(city)
        if not lat:
            speak("I could not find that city")
            return

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )

        data = requests.get(url, timeout=5).json()
        weather = data.get("current_weather")

        if not weather:
            speak("Weather data not available")
            return

        temp = weather["temperature"]
        wind = weather["windspeed"]

        speak(
            f"The current temperature in {city} is {temp} degree Celsius "
            f"with wind speed {wind} kilometers per hour"
        )
    except Exception:
        speak("Weather service is not available")

def tts_worker():
    while True:
        text = tts_queue.get()
        if silent_mode:
            print("Iris:", text)
            continue
        try:
            tts = gTTS(text)
            tts.save("voice.mp3")
            pygame.mixer.music.load("voice.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.music.unload()
            os.remove("voice.mp3")
        except:
            pass

threading.Thread(target=tts_worker, daemon=True).start()

def speak(text):
    print("Iris:", text)
    tts_queue.put(text)

def ai_chat(cmd):
    memory.append(cmd)
    try:
        res = model.generate_content("\n".join(memory[-8:]))
        reply = res.text.strip()
    except:
        reply = "AI response failed"
    memory.append(reply)
    speak(reply)

def confirm(cmd):
    speak(f"Did you say {cmd}? Say yes or no.")
    with sr.Microphone() as src:
        audio = recognizer.listen(src, phrase_time_limit=3)
        ans = recognizer.recognize_google(audio).lower()
        return "yes" in ans

def press(key):
    win32api.keybd_event(key,0,0,0)
    win32api.keybd_event(key,0,win32con.KEYEVENTF_KEYUP,0)

def open_app(cmd):
    try:
        apps = json.load(open("apps.json"))
        for k,v in apps.items():
            if k in cmd:
                subprocess.Popen(v)
                speak(f"Opening {k}")
                return
        speak("App not found")
    except:
        speak("apps.json missing")

def system_status():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    speak(f"CPU {cpu} percent, RAM {ram} percent")

def cpu_temp():
    try:
        w = wmi.WMI(namespace="root\\wmi")
        t = w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature
        speak(f"CPU temperature {(t/10-273.15):.1f} degree")
    except:
        speak("Temperature unavailable")

def window_info():
    hwnd = win32gui.GetForegroundWindow()
    speak(win32gui.GetWindowText(hwnd))

def volume(cmd):
    if "mute" in cmd: press(0xAD)
    if "up" in cmd: [press(0xAF) for _ in range(5)]
    if "down" in cmd: [press(0xAE) for _ in range(5)]

def process(cmd):
    global silent_mode
    cmd = cmd.lower()

    if "weather" in cmd:
        try:
            city = listen_city()
            get_weather_city(city)
        except Exception:
            speak("City not understood")
        return

    if "silent mode" in cmd:
        silent_mode = True
        speak("Silent mode enabled")
    elif "talk mode" in cmd:
        silent_mode = False
        speak("Voice mode enabled")
    elif "open" in cmd:
        open_app(cmd)
    elif "status" in cmd:
        system_status(); cpu_temp()
    elif "volume" in cmd or "mute" in cmd:
        volume(cmd)
    elif "time" in cmd:
        speak(datetime.datetime.now().strftime("%I:%M %p"))
    elif "date" in cmd:
        speak(datetime.date.today().strftime("%A %d %B %Y"))
    elif "what app" in cmd:
        window_info()
    elif "browser" in cmd:
        wb.open("https://google.com")
        speak("Opening browser")
    elif "exit" in cmd:
        speak("Goodbye")
        os._exit(0)
    else:
        ai_chat(cmd)

def listen_command():
    with sr.Microphone() as src:
        recognizer.adjust_for_ambient_noise(src, duration=0.5)
        try:
            audio = recognizer.listen(src, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            print("Command:", text)
            process(text)
        except sr.UnknownValueError:
            speak("I did not catch that")
        except sr.RequestError:
            speak("Speech service unavailable")
        except Exception as e:
            print("Listen Error:", e)
            speak("Something went wrong")


def wake_listener():
    global last_wake
    with sr.Microphone() as src:
        while True:
            audio = recognizer.listen(src, phrase_time_limit=3)
            try:
                txt = recognizer.recognize_google(audio).lower()
                if "iris" in txt and time.time() - last_wake > 4:
                    last_wake = time.time()
                    speak("Yes?")
                    listen_command()
            except sr.UnknownValueError:
                pass
            except:
                pass

def hotkey():
    while True:
        keyboard.wait("ctrl+alt+i")
        speak("Listening")
        listen_command()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    speak("Iris Pro is ready")
    threading.Thread(target=wake_listener, daemon=True).start()
    hotkey()
