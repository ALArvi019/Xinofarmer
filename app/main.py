"""
XinoFarmer - Web Interface Server
Servidor principal que arranca la interfaz web del bot
"""

import os
import sys
import socket
import webbrowser
import threading
import json
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager

# Intentar importar tkinter para popups (fallback a prints si no está disponible)
try:
    import tkinter as tk
    from tkinter import messagebox
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

try:
    from fastapi import FastAPI, Request, HTTPException, Depends
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
except ImportError:
    print("Error: FastAPI no está instalado. Ejecuta: pip install fastapi uvicorn jinja2 python-multipart")
    sys.exit(1)

# Local imports
from api.auth import get_auth, XinoFarmerAuth
from api.bot import get_bot, BotController, BotAction, BotStatus

# Configuración
XF_VERSION = "2.0.0"
DEFAULT_PORT = 47832  # Puerto "raro" para evitar conflictos
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR.parent / "setup.ini"


def show_popup(title: str, message: str, popup_type: str = "error"):
    """Muestra un popup al usuario. Usa tkinter si está disponible."""
    if HAS_TKINTER:
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        if popup_type == "error":
            messagebox.showerror(title, message)
        elif popup_type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
        root.destroy()
    else:
        print(f"[{popup_type.upper()}] {title}: {message}")


def is_port_in_use(port: int) -> bool:
    """Verifica si un puerto está en uso."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def find_available_port(start_port: int, max_attempts: int = 10) -> int:
    """Encuentra un puerto disponible empezando desde start_port."""
    for i in range(max_attempts):
        port = start_port + i
        if not is_port_in_use(port):
            return port
    return -1


def read_ini_file(filepath: Path) -> dict:
    """Lee un archivo INI y devuelve un diccionario."""
    config = {}
    if not filepath.exists():
        return config
    
    current_section = None
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(';') or line.startswith('#'):
                continue
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                config[current_section] = {}
            elif '=' in line and current_section:
                key, value = line.split('=', 1)
                config[current_section][key.strip()] = value.strip()
    return config


def write_ini_file(filepath: Path, config: dict):
    """Escribe un diccionario a un archivo INI."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for section, values in config.items():
            f.write(f'[{section}]\n')
            for key, value in values.items():
                f.write(f'{key}={value}\n')
            f.write('\n')


# Lifespan manager para inicialización y cleanup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print(f"XinoFarmer v{XF_VERSION} - Starting...")
    yield
    # Shutdown
    print("Shutting down...")
    bot = get_bot()
    bot.shutdown()


# Crear aplicación FastAPI
app = FastAPI(title="XinoFarmer", version=XF_VERSION, lifespan=lifespan)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos y templates
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ============== DEPENDENCY INJECTION ==============

def get_auth_service() -> XinoFarmerAuth:
    """Get authentication service."""
    return get_auth()


def get_bot_service() -> BotController:
    """Get bot controller service."""
    return get_bot()


# ============== RUTAS DE PÁGINAS ==============

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de login."""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "version": XF_VERSION
    })


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    auth: XinoFarmerAuth = Depends(get_auth_service)
):
    """Página principal del dashboard."""
    if not auth.is_authenticated:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "version": XF_VERSION,
            "error": "Please login first"
        })
    
    config = read_ini_file(CONFIG_FILE)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "version": XF_VERSION,
        "username": auth.current_user,
        "left_time": auth.left_time,
        "config": config
    })


# ============== API ENDPOINTS - AUTHENTICATION ==============

@app.post("/api/auth/login")
async def api_login(
    request: Request,
    auth: XinoFarmerAuth = Depends(get_auth_service),
    bot: BotController = Depends(get_bot_service)
):
    """API para login con autenticación encriptada."""
    data = await request.json()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    remember = data.get("remember", False)
    
    # Validación básica
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    # Validar formato de email
    import re
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Validar password
    if not re.match(r'^[a-zA-Z0-9]{8,14}$', password):
        raise HTTPException(status_code=400, detail="Password must be 8-14 alphanumeric characters")
    
    # Autenticar contra el servidor
    result = await auth.login(email, password)
    
    if result.success:
        # Inicializar el bot
        bot_init = await bot.initialize(email, result.left_time or "Unknown")
        
        return JSONResponse({
            "status": "ok",
            "message": result.message,
            "username": email,
            "left_time": result.left_time,
            "bot_initialized": bot_init
        })
    else:
        raise HTTPException(status_code=401, detail=result.message)


@app.post("/api/auth/register")
async def api_register(
    request: Request,
    auth: XinoFarmerAuth = Depends(get_auth_service)
):
    """API para registro."""
    data = await request.json()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    result = await auth.register(email, password)
    
    if result.success:
        return JSONResponse({
            "status": "ok",
            "message": result.message
        })
    else:
        raise HTTPException(status_code=400, detail=result.message)


@app.post("/api/auth/forgot-password")
async def api_forgot_password(
    request: Request,
    auth: XinoFarmerAuth = Depends(get_auth_service)
):
    """API para recuperar contraseña."""
    data = await request.json()
    email = data.get("email", "").strip()
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    result = await auth.forgot_password(email)
    
    if result.success:
        return JSONResponse({
            "status": "ok",
            "message": result.message
        })
    else:
        raise HTTPException(status_code=400, detail=result.message)


@app.post("/api/auth/logout")
async def api_logout(
    auth: XinoFarmerAuth = Depends(get_auth_service),
    bot: BotController = Depends(get_bot_service)
):
    """API para logout."""
    # Stop bot if running
    if bot.state.status == BotStatus.RUNNING:
        await bot.stop()
    
    # Logout
    auth.logout()
    
    return JSONResponse({"status": "ok"})


# ============== API ENDPOINTS - CONFIGURATION ==============

@app.get("/api/config")
async def api_get_config():
    """Obtener configuración actual."""
    config = read_ini_file(CONFIG_FILE)
    return JSONResponse(config)


@app.post("/api/config")
async def api_save_config(
    request: Request,
    bot: BotController = Depends(get_bot_service)
):
    """Guardar configuración."""
    data = await request.json()
    write_ini_file(CONFIG_FILE, data)
    bot.add_log("Configuration saved", "green")
    return JSONResponse({"status": "ok", "message": "Configuration saved"})


# ============== API ENDPOINTS - BOT CONTROL ==============

@app.post("/api/bot/start")
async def api_bot_start(
    request: Request,
    bot: BotController = Depends(get_bot_service)
):
    """Iniciar el bot."""
    data = await request.json()
    action_str = data.get("action", "SpotFarm")
    
    # Convert string to BotAction enum
    try:
        action = BotAction(action_str)
    except ValueError:
        action = BotAction.SPOT_FARM
    
    if bot.state.status == BotStatus.RUNNING:
        raise HTTPException(status_code=400, detail="Bot is already running")
    
    if not bot.state.cv_script_running:
        raise HTTPException(status_code=400, detail="Computer vision script is not running. Please restart the application.")
    
    success = await bot.start(action)
    
    if success:
        return JSONResponse({
            "status": "ok",
            "message": f"Bot started with action: {action.value}"
        })
    else:
        raise HTTPException(status_code=500, detail="Failed to start bot")


@app.post("/api/bot/stop")
async def api_bot_stop(
    bot: BotController = Depends(get_bot_service)
):
    """Detener el bot."""
    if bot.state.status == BotStatus.STOPPED:
        raise HTTPException(status_code=400, detail="Bot is not running")
    
    await bot.stop()
    return JSONResponse({"status": "ok", "message": "Bot stopped"})


@app.post("/api/bot/pause")
async def api_bot_pause(
    bot: BotController = Depends(get_bot_service)
):
    """Pausar/Reanudar el bot."""
    if bot.state.status == BotStatus.STOPPED:
        raise HTTPException(status_code=400, detail="Bot is not running")
    
    await bot.pause()
    
    return JSONResponse({
        "status": "ok",
        "message": f"Bot {'paused' if bot.state.status == BotStatus.PAUSED else 'resumed'}",
        "is_paused": bot.state.status == BotStatus.PAUSED
    })


@app.get("/api/bot/status")
async def api_bot_status(
    bot: BotController = Depends(get_bot_service)
):
    """Obtener estado actual del bot."""
    return JSONResponse(bot.state.to_dict())


@app.get("/api/logs")
async def api_get_logs(
    since: int = 0,
    bot: BotController = Depends(get_bot_service)
):
    """Obtener logs desde un índice específico."""
    logs = bot.get_logs(since)
    return JSONResponse({
        "logs": logs,
        "total": len(bot.state.logs)
    })


@app.post("/api/logs/clear")
async def api_clear_logs(
    bot: BotController = Depends(get_bot_service)
):
    """Limpiar logs."""
    bot.clear_logs()
    return JSONResponse({"status": "ok"})


def open_browser(port: int):
    """Abre el navegador en un hilo separado."""
    import time
    time.sleep(1)  # Esperar a que el servidor arranque
    webbrowser.open(f"http://localhost:{port}")


def main():
    """Punto de entrada principal."""
    print(f"XinoFarmer v{XF_VERSION}")
    print("=" * 40)
    
    # Verificar puerto
    port = DEFAULT_PORT
    if is_port_in_use(port):
        show_popup(
            "Port In Use",
            f"Port {port} is already in use. Looking for an available port...",
            "warning"
        )
        port = find_available_port(port + 1)
        if port == -1:
            show_popup(
                "Error",
                "Could not find an available port. Please close other applications and try again.",
                "error"
            )
            sys.exit(1)
        print(f"Using alternative port: {port}")
    
    print(f"Starting server on http://localhost:{port}")
    
    # Abrir navegador automáticamente
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    
    # Iniciar servidor
    try:
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
    except Exception as e:
        show_popup("Server Error", f"Could not start server: {str(e)}", "error")
        sys.exit(1)


if __name__ == "__main__":
    main()
