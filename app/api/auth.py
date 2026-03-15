"""
XinoFarmer - Authentication Module
Handles encrypted authentication against the backend server
"""

import os
import json
import base64
import hashlib
import time
from datetime import datetime, timezone
from typing import Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import httpx
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'cryptography', 'httpx'])
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import httpx


@dataclass
class AuthResult:
    """Result of an authentication attempt."""
    success: bool
    message: str
    left_time: Optional[str] = None
    token: Optional[str] = None


class XinoFarmerCrypto:
    """
    Encryption utilities compatible with the AutoIt/PHP backend.
    Uses AES-128 ECB mode for signature generation.
    """
    
    def __init__(self, master_key: str):
        """Initialize with the master key."""
        self.master_key = master_key.encode('utf-8')
        # Ensure key is 16 bytes for AES-128
        self.key = self.master_key[:16].ljust(16, b'\x00')
    
    def encrypt_aes128_ecb(self, data: str) -> str:
        """
        Encrypt data using AES-128 ECB mode.
        Returns base64-encoded encrypted data.
        Compatible with AutoIt's _Cryptshun function.
        """
        # Pad data to 16-byte blocks
        data_bytes = data.encode('utf-8')
        padding_length = 16 - (len(data_bytes) % 16)
        padded_data = data_bytes + bytes([padding_length] * padding_length)
        
        # Encrypt using AES-128 ECB
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return base64 encoded
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt_aes128_ecb(self, encrypted_b64: str) -> str:
        """
        Decrypt AES-128 ECB encrypted base64 data.
        """
        encrypted = base64.b64decode(encrypted_b64)
        
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted) + decryptor.finalize()
        
        # Remove PKCS7 padding
        padding_length = decrypted[-1]
        return decrypted[:-padding_length].decode('utf-8')
    
    def rc4_encrypt(self, data: str) -> bytes:
        """
        RC4 encryption compatible with AutoIt's StringEncrypt.
        """
        key = self.master_key
        S = list(range(256))
        j = 0
        
        # Key scheduling
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]
        
        # Encryption
        i = j = 0
        result = []
        for char in data.encode('utf-8'):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            k = S[(S[i] + S[j]) % 256]
            result.append(char ^ k)
        
        return bytes(result)
    
    def rc4_decrypt(self, data: bytes) -> str:
        """
        RC4 decryption (RC4 is symmetric).
        """
        key = self.master_key
        S = list(range(256))
        j = 0
        
        # Key scheduling
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]
        
        # Decryption
        i = j = 0
        result = []
        for byte in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            k = S[(S[i] + S[j]) % 256]
            result.append(byte ^ k)
        
        return bytes(result).decode('utf-8')
    
    def generate_auth_signature(self) -> Tuple[str, str]:
        """
        Generate the X-Auth signature header.
        Uses current datetime encrypted with AES-128 ECB.
        Returns (signature, timezone_string).
        """
        # Generate timestamp in format YYYYMMDDHHmmss
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S')
        
        # Encrypt the timestamp
        signature = self.encrypt_aes128_ecb(timestamp)
        
        # Get timezone offset
        local_tz = datetime.now(timezone.utc).astimezone().tzinfo
        offset = datetime.now(timezone.utc).astimezone().utcoffset()
        if offset:
            hours = int(offset.total_seconds() // 3600)
            tz_str = f"GMT{'+' if hours >= 0 else ''}{hours}"
        else:
            tz_str = "GMT+0"
        
        return signature, tz_str


class XinoFarmerAuth:
    """
    Authentication handler for XinoFarmer.
    Communicates with the backend server.
    """

    DOMAIN = os.environ.get("XF_DOMAIN", "example.com")
    MASTER_KEY = os.environ.get("XF_MASTER_KEY", "CHANGE_ME_16_CHARS")

    def __init__(self):
        """Initialize the authentication handler."""
        self.crypto = XinoFarmerCrypto(self.MASTER_KEY)
        self.current_user: Optional[str] = None
        self.left_time: Optional[str] = None
        self._session_token: Optional[str] = None
    
    def _get_auth_headers(self) -> dict:
        """Generate authentication headers for requests."""
        signature, timezone = self.crypto.generate_auth_signature()
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Auth": signature,
            "X-Timezone": timezone,
            "User-Agent": "XinoFarmer/2.0.0"
        }
    
    async def login(self, email: str, password: str) -> AuthResult:
        """
        Authenticate user against the Drupal 7 backend.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            AuthResult with success status and message
        """
        try:
            async with httpx.AsyncClient(verify=True, timeout=30.0) as client:
                response = await client.post(
                    f"https://{self.DOMAIN}/xf/login",
                    headers=self._get_auth_headers(),
                    data={"username": email, "password": password}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status", "")
                    message = data.get("message", "")
                    
                    if status == "ok":
                        self.current_user = email
                        self.left_time = message  # The message contains the expiration date
                        return AuthResult(
                            success=True,
                            message="Login successful",
                            left_time=message
                        )
                    else:
                        return AuthResult(
                            success=False,
                            message=message or "Login failed"
                        )
                else:
                    return AuthResult(
                        success=False,
                        message=f"Server error: {response.status_code}"
                    )
                    
        except httpx.ConnectError:
            return AuthResult(
                success=False,
                message="Could not connect to authentication server"
            )
        except httpx.TimeoutException:
            return AuthResult(
                success=False,
                message="Connection timed out"
            )
        except Exception as e:
            return AuthResult(
                success=False,
                message=f"Error: {str(e)}"
            )
    
    async def register(self, email: str, password: str) -> AuthResult:
        """
        Register a new user.
        
        Args:
            email: User's email address
            password: User's password (8-14 alphanumeric characters)
            
        Returns:
            AuthResult with success status and message
        """
        try:
            async with httpx.AsyncClient(verify=True, timeout=30.0) as client:
                response = await client.post(
                    f"https://{self.DOMAIN}/xf/register",
                    headers=self._get_auth_headers(),
                    data={"username": email, "password": password}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status", "")
                    message = data.get("message", "")
                    
                    if status == "ok":
                        return AuthResult(
                            success=True,
                            message="Registration successful. You can now login."
                        )
                    else:
                        return AuthResult(
                            success=False,
                            message=message or "Registration failed"
                        )
                else:
                    return AuthResult(
                        success=False,
                        message=f"Server error: {response.status_code}"
                    )
                    
        except Exception as e:
            return AuthResult(
                success=False,
                message=f"Error: {str(e)}"
            )
    
    async def forgot_password(self, email: str) -> AuthResult:
        """
        Request password reset.
        
        Args:
            email: User's email address
            
        Returns:
            AuthResult with success status and message
        """
        try:
            async with httpx.AsyncClient(verify=True, timeout=30.0) as client:
                response = await client.post(
                    f"https://{self.DOMAIN}/xf/forgot-password",
                    headers=self._get_auth_headers(),
                    data={"username": email}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status", "")
                    message = data.get("message", "")
                    
                    if status == "ok":
                        return AuthResult(
                            success=True,
                            message="Password reset email sent. Check your inbox and spam folder."
                        )
                    else:
                        return AuthResult(
                            success=False,
                            message=message or "Could not process request"
                        )
                else:
                    return AuthResult(
                        success=False,
                        message=f"Server error: {response.status_code}"
                    )
                    
        except Exception as e:
            return AuthResult(
                success=False,
                message=f"Error: {str(e)}"
            )
    
    def logout(self):
        """Clear the current session."""
        self.current_user = None
        self.left_time = None
        self._session_token = None
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated."""
        return self.current_user is not None


# Singleton instance
_auth_instance: Optional[XinoFarmerAuth] = None


def get_auth() -> XinoFarmerAuth:
    """Get the global authentication instance."""
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = XinoFarmerAuth()
    return _auth_instance
