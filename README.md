<a name="readme-top"></a>

<div align="center">
  <a href="https://github.com/Abdullahkhan000/Iris-Desktop-AI">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Iris Desktop AI</h3>

  <p align="center">
    An intelligent virtual assistant powered by Google Gemini.
    <br />
    <a href="https://github.com/Abdullahkhan000/Iris-Desktop-AI"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Abdullahkhan000/Iris-Desktop-AI/issues">Report Bug</a>
    ·
    <a href="https://github.com/Abdullahkhan000/Iris-Desktop-AI/issues">Request Feature</a>
  </p>
</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![OS](https://img.shields.io/badge/OS-Windows-blue?style=for-the-badge&logo=windows)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange?style=for-the-badge&logo=google)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

---

## 🤖 About The Project

**Iris-Desktop-AI** is a smart virtual assistant capable of controlling your desktop via **voice commands**.

It integrates **Google Gemini 1.5 Flash** to handle:

- complex queries  
- conversational context  
- dynamic AI responses  

The project is optimized for:

- 🪟 Windows

It manages:

- volume control
- app launching
- screenshots
- window management

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## ✨ Key Features

✔ AI-powered assistant  
✔ Voice control with wake word  
✔ Hotkeys  
✔ Desktop automation  

### Features List

- 🧠 **AI Intelligence:** Google Gemini 1.5 Flash
- 🎙️ **Wake Word:** “Iris”
- ⌨️ **Hotkeys**
  - Windows → `Ctrl + Alt + I`
- 🖥️ **System Control**
  - Volume up/down/mute
  - Minimize / maximize / close windows
  - Open apps (Notepad, Calculator, Terminal etc.)
  - Shutdown / restart
- 📸 **Utilities**
  - Take screenshots
  - Search files
  - CPU & RAM usage
  - Desktop notifications
- 🌍 **Multi-lingual**
  - English
  - Hindi
  - (Urdu support depends on STT model)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🚀 Getting Started

Follow these steps to run the project locally.

---

### 🔧 Prerequisites

- Python **3.10+**
- Microphone
- Google Gemini API Key

#### Windows specific
- PyAudio (see below)

---

### 📥 Installation

#### 1. Clone repository

```sh
git clone https://github.com/Abdullahkhan000/Iris-Desktop-AI.git
cd Iris-Desktop-AI
```

#### 2. Install packages

```sh
pip install -r requirements.txt
```

---

### 🎙️ PyAudio Installation Help

#### 🪟 Windows

If error occurs:

```sh
pip install pipwin
pipwin install pyaudio
```

If still not working:

- install Python **3.11**
- reinstall PyAudio

---

### 🔐 Configuration

Create `.env` in project root:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🗣️ How to Interact

Two ways to talk to Iris:

- Wake word → **“Iris”**
- Hotkey → Speak after pressing shortcut

Examples:

- “Iris, what time is it?”
- “Iris, open browser”

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 📝 Example Commands

| Category | Command Examples |
| :--- | :--- |
| **System** | “Volume up”, “Mute volume”, “System status”, “RAM and CPU status” |
| **Windows** | “Minimize window”, “Close window” |
| **Apps** | “Open Notepad”, “Open Calculator”, “Open Terminal” |
| **General** | “What is the time?”, “Open browser”, “Send notification”, “What is the weather” |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 📦 Dependencies

### 🎙️ Voice & Audio
* `SpeechRecognition` - For processing audio input.
* `gTTS` (Google Text-to-Speech) - To convert AI text response to audio.
* `PyAudio` - Necessary for microphone access and real-time listening.
* `pygame` - Used for audio playback and handling sound states.

### 🧠 AI & API
* `google-generativeai` - Official SDK for Google Gemini 1.5 Flash.
* `requests` - For handling web-based API requests.
* `python-decouple` - To manage API keys securely using `.env` files.

### 🤖 Automation & System Control
* `pyautogui` - For GUI automation (mouse and keyboard control).
* `keyboard` - To monitor and handle system-wide hotkeys.
* `psutil` - For monitoring CPU and RAM usage.
* `plyer` - For sending desktop notifications.

### 🪟 Windows Specific
* `pywin32` - (win32gui, win32con, win32api) To interact with Windows OS components.
* `WMI` - For deep system management and hardware interaction.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🤝 Contributing

Contributions are welcome:

1. Fork project  
2. Create feature branch  
3. Commit changes  
4. Push branch  
5. Open Pull Request  

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 📧 Contact

**Abdullah Khan**  
GitHub Profile: https://github.com/Abdullahkhan000

Project Link:  
https://github.com/Abdullahkhan000/Iris-Desktop-AI

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## ❤️ Support the Project

If this project saves you time or helps your work:

### 👉 Support via Patreon

[![Patreon](https://img.shields.io/badge/Support-Patreon-orange?style=flat&logo=patreon)](https://www.patreon.com/c/code2encoder)

Your support helps:
- Add new features
- Improve performance
- Maintain long-term updates

---

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it.

---

⭐ If you find this project useful, don’t forget to **star the repository**!

---

<div align="center">
  <p>🚀 This project is proudly made by <b>code2encoder aka / Shadow Dev</b> 🚀</p>
</div>
