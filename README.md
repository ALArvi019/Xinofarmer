# XinoFarmer

> **Automated farming bot for Diablo Immortal** using computer vision, image recognition, and emulator automation.

---

## DISCLAIMER

**THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY.**

The use of bots, automation tools, or any third-party software that interacts with online games **may violate the Terms of Service** of the game and can result in **permanent account bans**. By using this software, you acknowledge and accept the following:

- **The author(s) of this project are NOT responsible** for any consequences resulting from the use of this software, including but not limited to: account suspensions, bans, loss of in-game progress, or any other punitive actions taken by game developers or publishers.
- **Use at your own risk.** You are solely responsible for any actions taken with this tool.
- This project is intended as a **proof of concept** and a **learning resource** for topics such as computer vision, image recognition, desktop automation, and web application development.
- This project is **not affiliated with, endorsed by, or associated with** Blizzard Entertainment, NetEase, or any other game developer/publisher.
- The authors **do not encourage or condone** the use of bots or automation in online games in any way that violates the game's Terms of Service.

**If you choose to use this software in a live game environment, you do so entirely at your own risk.**

---

## What is XinoFarmer?

XinoFarmer is a bot designed to automate repetitive farming tasks in Diablo Immortal running on an Android emulator (LDPlayer). It uses a combination of:

- **Computer Vision (CV)** scripts written in Python for screen analysis and image recognition
- **AutoIt3** scripts for desktop-level input automation (mouse clicks, keyboard input)
- **A modern web UI** built with FastAPI for controlling and configuring the bot from a browser

### Supported Game Activities

| Activity | Description |
|----------|-------------|
| **Spot Farm** | Automatically farms a specific map location, killing monsters and looting items |
| **Dungeon** | Runs dungeon instances repeatedly (solo or team mode) |
| **Fishing** | Automates the fishing minigame (v1.0 legacy and v2.0 improved) |
| **Cyrangar** | Automates Cyrangar raids (endless fight or enter-and-exit mode) |

---

## Architecture

The project is composed of two main systems that work together:

```
┌─────────────────────────────────────────────────────┐
│                   Web Browser                        │
│              (localhost:47832)                        │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP
┌──────────────────▼──────────────────────────────────┐
│           FastAPI Web Server (app/)                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ Auth API │  │ Bot API  │  │ Config Manager    │  │
│  │(auth.py) │  │(bot.py)  │  │ (setup.ini)       │  │
│  └──────────┘  └────┬─────┘  └───────────────────┘  │
└─────────────────────┼───────────────────────────────┘
                      │ HTTP (port 9000)
┌─────────────────────▼───────────────────────────────┐
│        Computer Vision Script (xf.py/xf.exe)         │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ Screen   │  │ Image    │  │ Game              │  │
│  │ Capture  │  │ Matching │  │ Navigation        │  │
│  └──────────┘  └──────────┘  └───────────────────┘  │
└─────────────────────┬───────────────────────────────┘
                      │ Window API / ADB
┌─────────────────────▼───────────────────────────────┐
│          Android Emulator (LDPlayer)                  │
│              Diablo Immortal                          │
└─────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Web UI (`app/`)

A **FastAPI** application that provides:

- **Login/Registration** page with encrypted authentication against a backend server
- **Dashboard** with real-time bot control (Start, Stop, Pause)
- **Configuration panels** for each game activity (Spot Farm, Dungeon, Fishing, Cyrangar)
- **Emulator settings** (window name, LDPlayer path)
- **Telegram integration** for receiving notifications and screenshots
- **Activity log** console showing real-time bot actions

**Tech stack:** FastAPI, Jinja2 templates, vanilla JavaScript, CSS custom properties for theming.

#### 2. AutoIt Scripts (`inc/`)

The **legacy automation layer** written in AutoIt3:

- `XinoFarmer.au3` - Main entry point, version check, and login screen
- `inc/SETGlobals.au3` - Global configuration variables
- `inc/telegram.au3` - Telegram bot integration for notifications
- `inc/setupFile.au3` - GUI setup and configuration management
- `inc/JSONSetup.au3` - JSON-based configuration system for the GUI

#### 3. Computer Vision Scripts (`inc/scripts/MAIN/`)

Python scripts that handle the actual game interaction:

- `customsocketio.py` - Socket.IO client for real-time communication and session management
- `farming_spot.py` - Spot farming automation logic
- `endless_mode.py` - Cyrangar endless mode automation
- Additional scripts for dungeon running, fishing, map detection, monster detection, etc.

These scripts use **image recognition** to detect game elements on screen (buttons, menus, monsters, items) by comparing against reference images stored in `inc/img/`.

#### 4. Authentication System

The authentication uses **AES-128 ECB encryption** for secure communication with the backend:

1. A timestamp is encrypted with the master key and sent as an `X-Auth` header
2. The backend verifies the signature and processes the request
3. Compatible between the Python (`cryptography` library) and AutoIt (`_Crypt` UDF) implementations

---

## Project Structure

```
immortal_xinofarmer/
├── app/                          # FastAPI web server
│   ├── api/
│   │   ├── auth.py              # Authentication module (AES-128 encrypted auth)
│   │   └── bot.py               # Bot controller & CV script manager
│   ├── main.py                  # Server entry point, routes, config I/O
│   ├── static/
│   │   ├── css/style.css        # Dashboard & login styles
│   │   └── js/app.js            # Frontend application logic
│   ├── templates/
│   │   ├── login.html           # Login page
│   │   └── dashboard.html       # Main dashboard
│   └── requirements.txt         # Python dependencies
│
├── inc/                          # AutoIt scripts and resources
│   ├── SETGlobals.au3           # Global variables and configuration
│   ├── telegram.au3             # Telegram notification integration
│   ├── setupFile.au3            # GUI setup management
│   ├── JSONSetup.au3            # JSON configuration system
│   ├── scripts/MAIN/            # Computer vision Python scripts
│   │   ├── customsocketio.py    # Socket.IO real-time communication
│   │   ├── farming_spot.py      # Spot farming logic
│   │   ├── endless_mode.py      # Endless/Cyrangar mode logic
│   │   └── ...                  # Additional automation scripts
│   ├── img/                     # Reference images for recognition
│   │   ├── en/                  # English game client images
│   │   └── es/                  # Spanish game client images
│   ├── data/dll/                # Required DLL dependencies
│   └── UDF/                     # AutoIt User Defined Functions
│
├── setup.ini                    # Bot configuration file
├── XinoFarmer.au3              # Main AutoIt entry point
├── .env.example                 # Environment variables template
└── .gitignore
```

---

## Requirements

### System Requirements

- **OS:** Windows 10/11 (required for AutoIt and LDPlayer)
- **Python:** 3.8+
- **AutoIt3:** v3.3.16+ (for the legacy automation layer)
- **LDPlayer:** v9.x (Android emulator)
- **Diablo Immortal** installed on the emulator

### Python Dependencies

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
jinja2>=3.1.2
python-multipart>=0.0.6
httpx>=0.25.0
cryptography>=41.0.0
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/immortal_xinofarmer.git
cd immortal_xinofarmer
```

### 2. Set up Python environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r app/requirements.txt
```

### 3. Configure environment variables

```bash
copy .env.example .env
```

Edit `.env` with your actual values:

```env
XF_DOMAIN=your-backend-domain.com
XF_MASTER_KEY=your16charkey!!
```

### 4. Configure the bot

Edit `setup.ini` to match your setup:

- **VMName**: The window title of your LDPlayer instance
- **LDPath**: Full path to `ldconsole.exe`
- **Language**: `English` or `Spanish` (must match your game client language)
- **Telegram Token**: Your Telegram bot token (if using notifications)

### 5. Set up LDPlayer

1. Install LDPlayer 9
2. Install Diablo Immortal inside the emulator
3. Set the emulator resolution to **960x540** (required for image recognition)
4. Make sure the game is in the language matching your `setup.ini` Language setting

---

## Usage

### Starting the Web UI

```bash
cd app
python main.py
```

This will:
1. Start the FastAPI server on `http://localhost:47832`
2. Automatically open your browser to the login page

### Using the Dashboard

1. **Login** with your credentials
2. Select the **action** you want to automate (Spot Farm, Dungeon, etc.)
3. Configure the settings for that action in the corresponding tab
4. Click **Save** to persist your configuration
5. Click **Start** to begin automation
6. Monitor progress in the **Activity Log**
7. Use **Pause/Stop** to control the bot

### Running the Legacy AutoIt Bot

If you prefer the classic desktop GUI:

1. Open `XinoFarmer.au3` with AutoIt3
2. Or compile it to `.exe` and run it directly

---

## Configuration Reference

### setup.ini Sections

| Section | Key | Description | Values |
|---------|-----|-------------|--------|
| **Main** | Action | Default action | SpotFarm, Dungeon, Fish, Fish2.0, Cyrangar |
| | Player | Character slot | 1-5 |
| | VMName | Emulator window title | String |
| | LDPath | Path to ldconsole.exe | File path |
| | Language | Game language | English, Spanish |
| | StopBotAfter | Auto-stop timer (0=never) | Minutes |
| **SpotFarm** | SpotFarmMap | Map to farm | Ashwold, DarkWood, Library, etc. |
| | SpotFarmDifficulty | Game difficulty | H1-H8, I1-I5 |
| **Dungeon** | name | Dungeon name | Kikuras, MadKingsBreach, etc. |
| | Team_solo | Play mode | Solo, Team |
| **Fish2** | Fish2Type | Fish rarity target | Gold, Blue, Any |
| | Maps | Fishing map | Bilefen, Ashwold, etc. |
| **Telegram** | Active | Enable notifications | Yes, No |
| | Token | Your Telegram bot token | String |
| **Cyrangar** | Mode | Raid mode | Endless, EnterAndExit |

---

## How It Works (Technical Details)

### Image Recognition Pipeline

1. **Screen Capture**: The CV script captures the emulator window
2. **Template Matching**: OpenCV `matchTemplate` compares captured frames against reference images in `inc/img/`
3. **Decision Making**: Based on what's detected on screen, the bot decides the next action
4. **Input Simulation**: Commands are sent to the emulator via LDPlayer's console API or Windows API

### Authentication Flow

```
Client                          Backend Server
  │                                    │
  │  POST /xf/login                    │
  │  X-Auth: AES128(timestamp)         │
  │  X-Timezone: GMT+X                 │
  │  Body: username + password         │
  │───────────────────────────────────▶│
  │                                    │
  │  {status: "ok", message: "..."}    │
  │◀───────────────────────────────────│
```

### Communication Between Components

- **Web UI → FastAPI**: Standard HTTP REST API calls
- **FastAPI → CV Script**: HTTP on localhost:9000 (command/response protocol)
- **CV Script → Emulator**: Windows API / LDPlayer console commands
- **Real-time sync**: Socket.IO for session management and multi-device coordination

---

## Telegram Integration

XinoFarmer can send notifications to Telegram:

1. Create a Telegram bot via [@BotFather](https://t.me/BotFather)
2. Get your bot token
3. Set the token in `setup.ini` under `[Telegram] Token`
4. Enable Telegram in the dashboard settings
5. Send `/configure` to your bot to link your account

Notifications include:
- Bot start/stop events
- Farming statistics
- Screenshot captures on demand

---

## Supported Languages

The bot supports two game client languages:

- **English** - Reference images in `inc/img/en/`
- **Spanish** - Reference images in `inc/img/es/`

Make sure the `Language` setting in `setup.ini` matches your in-game language, as the bot relies on image matching to detect UI elements.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Bot can't find the emulator | Verify `VMName` matches the exact window title |
| Image recognition fails | Ensure emulator resolution is 960x540 |
| CV script won't start | Check Python dependencies and DLL path |
| Authentication fails | Verify `.env` configuration and backend availability |
| Port 47832 in use | The server will auto-find an available port |

---

## License

This project is provided as-is, without warranty of any kind. See the [DISCLAIMER](#disclaimer) above.

---

## Contributing

This is an archived/educational project. Feel free to fork and adapt it for your own learning purposes.

**Remember: Using bots in online games can get your account banned. This project exists purely for educational purposes related to computer vision, automation, and web development.**
