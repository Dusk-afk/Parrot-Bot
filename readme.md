# 🦜 Parrot Bot

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Discord](https://img.shields.io/badge/Discord-Py--Cord-5865F2?logo=discord)
![License](https://img.shields.io/badge/License-MIT-green)
![GTTS](https://img.shields.io/badge/TTS-Google--TTS-4285F4?logo=google)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Audio-007808?logo=ffmpeg)

Parrot Bot is a Discord bot that monitors voice channel activities and greets users with real-time voice messages in multiple languages. Originally developed by Dusk#2577 & arsh#5480 on 18/03/2022, Parrot Bot listens for join and leave events in voice channels and speaks accordingly in either English or Hindi. Soon, more languages will be supported!

## ✨ Features

- **🎙️ Voice Channel Activity Monitoring:**  
  Detects when a user joins or leaves a voice channel and plays a dynamic greeting message.  
  Refer to [`services/client.py`](../../../d:/Programming/Parrot-Bot/services/client.py).

- **🗣️ Text-to-Speech (TTS):**  
  Uses Google Text-to-Speech (gTTS) for generating audio from text.  
  See [`services/audio_service.py`](../../../d:/Programming/Parrot-Bot/services/audio_service.py) and [`services/FFmpegPCMAudioGTTS.py`](../../../d:/Programming/Parrot-Bot/services/FFmpegPCMAudioGTTS.py).

- **⚙️ Customizable Guild Settings:**  
  Each Discord guild can customize the language (English/Hindi) and enable/disable Parrot’s "say" command.  
  Check out [`services/db.py`](../../../d:/Programming/Parrot-Bot/services/db.py) and [`services/parrot_cog.py`](../../../d:/Programming/Parrot-Bot/services/parrot_cog.py).

- **🤖 Slash Commands:**  
  Engage with the bot easily using slash commands such as:
  - `/start` – Connect Parrot to your current voice channel.
  - `/stop` – Disconnect Parrot.
  - `/hello` – Test if Parrot can speak.
  - `/say` – Ask Parrot to repeat your message.
  - `/config` – Manage settings (language and say command).
  - `/shutup` – Stop any ongoing speech.
  - `/test` – Check if the bot is running.
  - `/help` – Display all available commands.
  
  All command logic can be found in [`services/parrot_cog.py`](../../../d:/Programming/Parrot-Bot/services/parrot_cog.py).

## 🚀 Installation

### 📋 Prerequisites

- Python 3.10  
- ffmpeg (installed in your OS or provided via Docker)
- A valid Discord bot token in the [`.env`](../../../d:/Programming/Parrot-Bot/.env) file

### 💻 Local Setup

1. **📥 Install Dependencies:**  
   Run:
   ```sh
   pip install -r requirements.txt
   ```
   This installs required packages such as `py-cord`, `gTTS`, and others.
See requirements.txt.

2. **▶️ Run the Bot:**  
   Start the bot by running:
   ```sh
   python main.py
   ```
   The bot should now be online and ready to greet users in your Discord server!

### 🐳 Docker Setup
The project comes with a Dockerfile and docker-compose.yaml for containerized deployment.
1. **Build and Run with Docker Compose**
    ```sh
    docker-compose up --build
    ```
    This command builds the Docker image and starts the bot in a container.

### 🔧 Configuration & Database
- Environment Variables:
The bot token is stored in the .env file.

- Guild Settings Database:
Guild-specific configurations (like language and say command status) are managed via a JSON file (db.json) and handled by the services/db.py module.

## 📬 Contact
For support or contributions, please contact the original developers at Dusk#2577 or arsh#5480.