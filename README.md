Bro.ai – Intelligent Virtual Personal Assistant
Overview

Bro.ai is an intelligent virtual personal assistant designed to act like a supportive digital friend who can talk, think, understand, create, and control your system in real time. It combines natural conversation, automation, AI-powered creativity, and a visually modern user interface into one seamless desktop application. Bro.ai listens to your voice, responds naturally, generates images, retrieves real-world information, writes content, opens and controls apps, plays music, and performs system-level actions while maintaining a friendly personality.

Frontend:


The frontend of Bro.ai is built using HTML, CSS, and JavaScript, presented inside a PyWebView desktop window. The interface includes animated neon glow effects, smooth transitions, a landing page, login panel, customizable profile system, and a dual-screen environment that switches between home view and chat view. The design places emphasis on clarity and user experience, with a real-time chat display that reads from a JSON file and updates automatically. Microphone activation is visually animated, message bubbles are styled with modern gradients, and all interactions feel polished and futuristic.

Backend:



The backend is developed entirely in Python, connecting multiple advanced modules into a single intelligent system. It uses PyWebView for UI integration, SpeechRecognition and PyAudio for capturing voice, Edge-TTS for generating natural speech, Pillow for image processing, PyAutoGUI and Psutil for system automation, Requests for API communication, Langdetect for language detection, and Asyncio for parallel task execution. The backend also includes a custom Query Classifier, a chat generation engine, a real-time search engine, an image generation module, and an automation controller that handles computer-level tasks. Every message or voice command flows through this backend, which intelligently decides the correct action to perform.

How Bro.ai Works:
Bro.ai continuously monitors both voice and text input. When a user speaks, the backend converts audio into text, detects the language, and classifies the intent. If the request is conversational, Bro.ai generates a natural chat response. If real-time information is needed, it fetches live data from the web. When users describe images, Bro.ai generates them using an integrated AI model. If the user gives an instruction such as opening apps, controlling volume, toggling WiFi or Bluetooth, playing songs, or writing content, Bro.ai performs the required automation instantly. The final response is spoken aloud using a human-like voice and saved into the chat history to maintain smooth synchronization with the interface.

How to Run:



Running Bro.ai is simple. After downloading or cloning the project, install the necessary Python libraries, set the correct path for the chat JSON file, and launch the main.py script. The application will open automatically in a desktop window using PyWebView and initialize all backend modules. Once the interface appears, users can type messages or activate the microphone to speak naturally with Bro.ai.

Start Command:



Install the required dependencies:
pip install -r requirements.txt

To start the assistant, activate your environment and run the following command in your terminal

python main.py
This single command launches the interface, loads the backend, and starts the real-time assistant engine with full functionality.

Developer:


© All rights reserved by Srajan Shetty
<p align="center">
  <img src="interface.png" width="900">
</p>
<p align="center">
  <img src="home.mp4" width="900">
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





