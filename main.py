# =====================================================
#  This Iris Desktop Made By ShadowDev / code2encoder
# =====================================================

import os
import warnings
import logging

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
warnings.filterwarnings("ignore", category=FutureWarning)
logging.basicConfig(level=logging.ERROR)

import subprocess
import webbrowser as wb
import datetime
import pyautogui
import psutil
import keyboard
import threading
import speech_recognition as sr
from gtts import gTTS
import pygame
from decouple import config
from plyer import notification
import requests
import win32gui
import win32con
import win32api
import wmi

pygame.mixer.init()
recognizer = sr.Recognizer()

import google.generativeai as genai
GOOGLE_KEY = config("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_KEY)
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
    except Exception:
        pass


def ai(text):
    memory.append(text)
    try:
        response = model.generate_content("\n".join(memory[-8:]))
        reply = response.text
    except Exception:
        reply = "Sorry, I couldn't process that."
    memory.append(reply)
    speak(reply)

def press_key(key):
    win32api.keybd_event(key, 0, 0, 0)
    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)


def control_volume(action):
    action = action.lower()
    if action == "mute" or action == "unmute":
        press_key(0xAD)
        speak(f"Volume {action}d")
    elif "up" in action:
        for _ in range(5):
            press_key(0xAF)
        speak("Volume increased")
    elif "down" in action:
        for _ in range(5):
            press_key(0xAE)
        speak("Volume decreased")


def window_action(action):
    hwnd = win32gui.GetForegroundWindow()
    if "minimize" in action:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    elif "maximize" in action:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    elif "close" in action:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    speak("Done")


def open_any_app(name):
    apps = {
        "notepad": "notepad.exe",
        "cmd": "cmd.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "task manager": "taskmgr.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    }
    for key, exe in apps.items():
        if key in name:
            subprocess.Popen(exe, shell=True)
            speak(f"Opening {key}")
            return
    speak("Application not found")


def get_system_status():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    speak(f"CPU at {cpu} percent, RAM at {ram} percent")
    get_cpu_temperature()

def get_cpu_temperature():
    try:
        w = wmi.WMI(namespace="root\wmi")
        temp_info = w.MSAcpi_ThermalZoneTemperature()
        if temp_info:
            temp_c = temp_info[0].CurrentTemperature / 10 - 273.15
            speak(f"The CPU temperature is {temp_c:.1f} degree Celsius")
        else:
            speak("Could not read CPU temperature")
    except Exception as e:
        speak("Error reading CPU temperature")

def process(cmd):
    cmd = cmd.lower().strip()

    if "weather" in cmd:
        try:
            city = listen_city()
            get_weather_city(city)
        except Exception:
            speak("City not understood")
        return

    if "cpu temperature" in cmd or "temperature" in cmd:
        get_cpu_temperature()
    elif "status" in cmd:
        get_system_status()

    if cmd in ["mute", "unmute"] or "volume" in cmd:
        control_volume(cmd)
    elif "time" in cmd:
        speak(datetime.datetime.now().strftime("%I:%M %p"))
    elif "date" in cmd:
        speak(datetime.date.today().strftime("%A %d %B %Y"))
    elif "status" in cmd:
        get_system_status()
    elif "open" in cmd:
        open_any_app(cmd)
    elif "browser" in cmd:
        wb.open("https://google.com")
        speak("Opening browser")

    elif "exit" in cmd:
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
                text = recognizer.recognize_google(audio).lower()
                if "iris" in text:
                    speak("Yes?")
                    listen_for_command()
            except Exception:
                continue


def listen_for_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            print("Command:", text)
            process(text)
        except Exception:
            speak("Say that again please")


def hotkey_listener():
    while True:
        keyboard.wait("ctrl+alt+i")
        speak("Listening")
        listen_for_command()

if __name__ == "__main__":
    show_banner()
    speak("Iris is ready")
    threading.Thread(target=wake_word_listener, daemon=True).start()
    hotkey_listener()