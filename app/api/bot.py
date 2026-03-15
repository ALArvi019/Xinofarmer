"""
XinoFarmer - Bot Controller Module
Manages the computer vision Python scripts and bot operations
"""

import os
import sys
import subprocess
import signal
import asyncio
import json
from pathlib import Path
from typing import Optional, Dict, Any, Callable, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
import time

try:
    import httpx
except ImportError:
    import subprocess as sp
    sp.check_call(['pip', 'install', 'httpx'])
    import httpx


class BotAction(str, Enum):
    """Available bot actions."""
    SPOT_FARM = "SpotFarm"
    DUNGEON = "Dungeon"
    FISH = "Fish"
    FISH_V2 = "Fish2.0"
    CYRANGAR = "Cyrangar"
    RIFT = "Rift"


class BotStatus(str, Enum):
    """Bot status states."""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    STARTING = "starting"


@dataclass
class LogEntry:
    """A single log entry."""
    timestamp: str
    message: str
    color: str = "default"
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "timestamp": self.timestamp,
            "message": self.message,
            "color": self.color
        }


@dataclass
class BotState:
    """Current state of the bot."""
    status: BotStatus = BotStatus.STOPPED
    current_action: Optional[BotAction] = None
    start_time: Optional[datetime] = None
    username: Optional[str] = None
    left_time: Optional[str] = None
    logs: List[LogEntry] = field(default_factory=list)
    cv_script_running: bool = False
    cv_script_pid: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "current_action": self.current_action.value if self.current_action else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "username": self.username,
            "left_time": self.left_time,
            "cv_script_running": self.cv_script_running
        }


class CVScriptController:
    """
    Controller for the Computer Vision Python scripts.
    Manages xf.exe/xf.py which runs on port 9000.
    """
    
    CV_SCRIPT_PORT = 9000
    CV_SCRIPT_NAME = "xf.exe"  # Compiled script, use xf.py for development
    CV_SCRIPT_TIMEOUT = 30  # seconds
    
    def __init__(self, scripts_dir: Path):
        """
        Initialize the CV Script Controller.
        
        Args:
            scripts_dir: Path to the inc/scripts/MAIN directory
        """
        self.scripts_dir = scripts_dir
        self.process: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()
    
    def _get_script_path(self) -> Path:
        """Get the path to the CV script."""
        # Try compiled version first, then Python script
        exe_path = self.scripts_dir / self.CV_SCRIPT_NAME
        if exe_path.exists():
            return exe_path
        
        py_path = self.scripts_dir / "xf.py"
        if py_path.exists():
            return py_path
        
        raise FileNotFoundError(f"CV script not found in {self.scripts_dir}")
    
    def is_running(self) -> bool:
        """Check if the CV script is currently running."""
        if self.process is None:
            return False
        return self.process.poll() is None
    
    def start(self, username: str) -> bool:
        """
        Start the CV script process.
        
        Args:
            username: The authenticated username
            
        Returns:
            True if started successfully, False otherwise
        """
        with self._lock:
            if self.is_running():
                return True
            
            try:
                script_path = self._get_script_path()
                
                # Prepare environment with DLL path
                env = os.environ.copy()
                dll_path = self.scripts_dir.parent.parent / "data" / "dll"
                if dll_path.exists():
                    current_path = env.get("PATH", "")
                    env["PATH"] = f"{dll_path}{os.pathsep}{current_path}"
                
                # Start the script
                if script_path.suffix == ".py":
                    cmd = [sys.executable, str(script_path), "fromXF", username]
                else:
                    cmd = [str(script_path), "fromXF", username]
                
                self.process = subprocess.Popen(
                    cmd,
                    cwd=str(self.scripts_dir),
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                )
                
                # Wait a bit to check if it started correctly
                time.sleep(2)
                
                if self.process.poll() is not None:
                    # Process exited immediately - error
                    stderr = self.process.stderr.read().decode('utf-8', errors='ignore')
                    raise RuntimeError(f"CV script failed to start: {stderr}")
                
                return True
                
            except Exception as e:
                print(f"Error starting CV script: {e}")
                return False
    
    def stop(self):
        """Stop the CV script process."""
        with self._lock:
            if self.process is not None and self.is_running():
                try:
                    if sys.platform == "win32":
                        self.process.terminate()
                    else:
                        self.process.send_signal(signal.SIGTERM)
                    
                    # Wait for graceful shutdown
                    try:
                        self.process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self.process.kill()
                        self.process.wait()
                except Exception as e:
                    print(f"Error stopping CV script: {e}")
                finally:
                    self.process = None
    
    async def send_command(self, command: str, timeout: float = 10.0) -> Optional[str]:
        """
        Send a command to the CV script via HTTP.
        
        Args:
            command: The command string to send
            timeout: Request timeout in seconds
            
        Returns:
            Response from the CV script or None on error
        """
        if not self.is_running():
            return None
        
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    f"http://127.0.0.1:{self.CV_SCRIPT_PORT}/xf",
                    content=command,
                    headers={"Content-Type": "text/plain"}
                )
                
                if response.status_code == 200:
                    return response.text
                else:
                    return None
                    
        except Exception as e:
            print(f"Error sending command to CV script: {e}")
            return None
    
    async def check_version(self, expected_version: str = "1.7.6") -> bool:
        """
        Check if the CV script version matches.
        
        Args:
            expected_version: Expected version string
            
        Returns:
            True if versions match
        """
        response = await self.send_command("XF_2ndScript_Version")
        return response == expected_version if response else False
    
    async def ping(self) -> bool:
        """
        Check if the CV script is responding.
        
        Returns:
            True if CV script responds correctly
        """
        response = await self.send_command("XF_2ndScript_Start")
        return response == "XF_2ndScript_Start" if response else False


class BotController:
    """
    Main bot controller that orchestrates all bot operations.
    """
    
    VERSION = "2.0.0"
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize the bot controller.
        
        Args:
            base_dir: Base directory of the XinoFarmer installation
        """
        if base_dir is None:
            # Try to find the base directory
            current = Path(__file__).parent.parent.parent
            if (current / "inc" / "scripts" / "MAIN").exists():
                base_dir = current
            else:
                base_dir = Path.cwd()
        
        self.base_dir = base_dir
        self.scripts_dir = base_dir / "inc" / "scripts" / "MAIN"
        self.config_file = base_dir / "setup.ini"
        
        # Initialize state
        self.state = BotState()
        
        # Initialize CV script controller
        self.cv_controller = CVScriptController(self.scripts_dir)
        
        # Log listeners
        self._log_listeners: List[Callable[[LogEntry], None]] = []
        
        # Background tasks
        self._log_poll_task: Optional[asyncio.Task] = None
    
    def add_log(self, message: str, color: str = "default"):
        """Add a log entry."""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            message=message,
            color=color
        )
        self.state.logs.append(entry)
        
        # Limit log size
        if len(self.state.logs) > 1000:
            self.state.logs = self.state.logs[-500:]
        
        # Notify listeners
        for listener in self._log_listeners:
            try:
                listener(entry)
            except Exception:
                pass
    
    def add_log_listener(self, listener: Callable[[LogEntry], None]):
        """Add a log listener callback."""
        self._log_listeners.append(listener)
    
    def remove_log_listener(self, listener: Callable[[LogEntry], None]):
        """Remove a log listener callback."""
        if listener in self._log_listeners:
            self._log_listeners.remove(listener)
    
    def get_logs(self, since_index: int = 0) -> List[Dict[str, str]]:
        """Get logs since a specific index."""
        return [log.to_dict() for log in self.state.logs[since_index:]]
    
    def clear_logs(self):
        """Clear all logs."""
        self.state.logs.clear()
        self.add_log("Logs cleared", "default")
    
    async def initialize(self, username: str, left_time: str) -> bool:
        """
        Initialize the bot after successful login.
        
        Args:
            username: Authenticated username
            left_time: Subscription expiration time
            
        Returns:
            True if initialization successful
        """
        self.state.username = username
        self.state.left_time = left_time
        self.state.status = BotStatus.STARTING
        
        self.add_log("Initializing bot...", "blue")
        
        # Check if scripts directory exists
        if not self.scripts_dir.exists():
            self.add_log(f"Scripts directory not found: {self.scripts_dir}", "red")
            self.state.status = BotStatus.ERROR
            return False
        
        # Start CV script
        self.add_log("Starting computer vision script...", "blue")
        if self.cv_controller.start(username):
            self.state.cv_script_running = True
            self.state.cv_script_pid = self.cv_controller.process.pid if self.cv_controller.process else None
            
            # Wait and check if it's responding
            await asyncio.sleep(3)
            
            if await self.cv_controller.ping():
                self.add_log("Computer vision script is running OK.", "green")
                
                # Check version
                if await self.cv_controller.check_version():
                    self.add_log("Version of computer vision script is OK.", "green")
                else:
                    self.add_log("Version mismatch. Consider updating.", "yellow")
                
                # Send username
                await self.cv_controller.send_command(f"XF_2ndScript_chUser|{username}")
                self.add_log("Username sent to CV script.", "green")
                
                self.state.status = BotStatus.STOPPED
                return True
            else:
                self.add_log("Computer vision script is not responding.", "red")
        else:
            self.add_log("Failed to start computer vision script.", "red")
        
        self.state.status = BotStatus.ERROR
        return False
    
    async def start(self, action: BotAction, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Start the bot with a specific action.
        
        Args:
            action: The action to perform
            config: Optional configuration override
            
        Returns:
            True if started successfully
        """
        if self.state.status == BotStatus.RUNNING:
            self.add_log("Bot is already running.", "yellow")
            return False
        
        if not self.state.cv_script_running:
            self.add_log("Computer vision script is not running. Cannot start.", "red")
            return False
        
        self.state.current_action = action
        self.state.start_time = datetime.now()
        self.state.status = BotStatus.RUNNING
        
        self.add_log(f"Bot started with action: {action.value}", "green")
        self.add_log(f"Press F9 to terminate script.", "orange")
        
        # Send start command to CV script based on action
        command_map = {
            BotAction.SPOT_FARM: "fromXF|startfarmingspot",
            BotAction.DUNGEON: "fromXF|startdungeon",
            BotAction.FISH: "fromXF|startfishing",
            BotAction.FISH_V2: "fromXF|startfishingv2",
            BotAction.CYRANGAR: "fromXF|startcyrangar",
        }
        
        if action in command_map:
            config_data = self._load_config()
            vm_name = config_data.get("Main", {}).get("VMName", "LDPlayer")
            
            # Build command with config
            cmd = f"{command_map[action]}|{vm_name}"
            await self.cv_controller.send_command(cmd)
        
        return True
    
    async def stop(self) -> bool:
        """Stop the bot."""
        if self.state.status == BotStatus.STOPPED:
            self.add_log("Bot is already stopped.", "yellow")
            return False
        
        # Send stop command to CV script
        config_data = self._load_config()
        vm_name = config_data.get("Main", {}).get("VMName", "LDPlayer")
        await self.cv_controller.send_command(f"fromXF|stopfarmingspot|{vm_name}")
        
        self.state.status = BotStatus.STOPPED
        self.state.current_action = None
        self.state.start_time = None
        
        self.add_log("Bot stopped.", "orange")
        return True
    
    async def pause(self) -> bool:
        """Toggle pause state."""
        if self.state.status == BotStatus.STOPPED:
            self.add_log("Bot is not running. Cannot pause.", "yellow")
            return False
        
        if self.state.status == BotStatus.PAUSED:
            self.state.status = BotStatus.RUNNING
            self.add_log("Bot resumed.", "green")
        else:
            self.state.status = BotStatus.PAUSED
            self.add_log("Bot paused.", "yellow")
        
        return True
    
    def shutdown(self):
        """Shutdown the bot and cleanup resources."""
        self.add_log("Shutting down...", "orange")
        
        # Stop CV script
        self.cv_controller.stop()
        self.state.cv_script_running = False
        
        self.state.status = BotStatus.STOPPED
        self.state.current_action = None
    
    def _load_config(self) -> Dict[str, Dict[str, str]]:
        """Load configuration from setup.ini."""
        config = {}
        
        if not self.config_file.exists():
            return config
        
        current_section = None
        with open(self.config_file, 'r', encoding='utf-8') as f:
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
    
    def save_config(self, config: Dict[str, Dict[str, str]]):
        """Save configuration to setup.ini."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            for section, values in config.items():
                f.write(f'[{section}]\n')
                for key, value in values.items():
                    f.write(f'{key}={value}\n')
                f.write('\n')
        
        self.add_log("Configuration saved.", "green")


# Singleton instance
_bot_instance: Optional[BotController] = None


def get_bot() -> BotController:
    """Get the global bot controller instance."""
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = BotController()
    return _bot_instance
