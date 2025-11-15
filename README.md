Bro.ai – Intelligent Virtual Personal Assistant
Full-stack desktop AI assistant: Python backend + HTML/CSS/JS frontend (PyWebView).
Overview

Backend: Python AI engine using Groq for chat/writing, Google Search API for real-time info, Hugging Face for image generation, and system automation modules.
Frontend: HTML/CSS/JS UI rendered inside a PyWebView desktop window.
Purpose: Natural conversation, system control, AI-powered writing, image generation, and real-time search.

Tech stack
Frontend

HTML

CSS

JavaScript

PyWebView

Backend

Python

Groq API (chat + writing + intent-based responses)

Google Search (Python API) for real-time results

Hugging Face Inference API for image generation

SpeechRecognition, PyAudio

Edge-TTS

Pillow

PyAutoGUI, psutil

requests

langdetect

asyncio

Quick start (development)
1. Install dependencies
pip install -r requirements.txt

2. Run the assistant
python main.py


Frontend launches automatically inside PyWebView.
Backend loads Groq, Google Search, HuggingFace, voice recognition, and automation engine.

Project structure (important files)
backend/ — Python AI engine
  ├── chat/ — Groq chat + writing
  ├── search/ — Google Python Search API
  ├── image/ — Hugging Face image generator
  ├── automation/ — system-level actions
  ├── speech/ — STT + TTS
  ├── classifier/ — intent detection
  └── engine.py — main logic processor

frontend/ — HTML/CSS/JS interface
  ├── index.html — UI layout
  ├── style.css — neon theme
  ├── script.js — chat rendering + mic animations
  └── profile/ — user profiles

main.py — application entry point  
chat.json — real-time chat history  
requirements.txt — dependencies  

Core features

Groq-powered chat (ultra-fast reasoning)

Groq-powered writing (emails, stories, content)

Google Search API for real-time information

Hugging Face image generation

Voice interaction (STT + TTS)

Automation (apps, volume, WiFi, Bluetooth, system tasks)

Modern neon UI with live chat updates

Internal “API-style” actions (handled by classifier)
Intent	Engine Used	Description
chat	Groq	Friendly conversational response
write	Groq	Generates content, text, emails, etc.
search	Google Search Python API	Live real-world data
generate_image	Hugging Face	AI image generation
automate	Python automation	Apps, system settings, controls

Developer

© All rights reserved by Srajan Shetty


<p align="center">
  <img src="interface.png" width="900">
</p>
<p align="center">
  <img src="home.png" width="900">
</p>
<p align="center">
  <img src="chats1.png" width="900">
</p>

<p align="center">
  <img src="chat.png" width="900">
</p>
<p align="center">
  <img src="chats.png" width="900">
</p>
<p align="center">
  <img src="settings.png" width="900">
</p>





