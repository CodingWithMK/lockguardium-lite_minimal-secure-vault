import os, base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_PATH = "salt.bin"

def load_or_create_salt() -> bytes:
    """Load the salt from a file or create a new one if it does not exist."""
    if os.path.exists(SALT_PATH):
        return open(SALT_PATH, "rb").read()
    salt = os.urandom(16)
    with open(SALT_PATH, "wb") as f:
        f.write(salt)
    return salt

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a key from the password and salt using PBKDF2."""
    pwd = password.encode("utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000, 
    )
    raw_key = kdf.derive(pwd)
    return base64.urlsafe_b64encode(raw_key) # Ensure the key is URL-safe and 32 bytes long

def encrypt_password(key: bytes, plaintext: str) -> bytes:
    """Encrypt a plaintext password using the provided key."""
    fernet = Fernet(key)
    return fernet.encrypt(plaintext.encode("utf-8"))

def decrypt_password(key: bytes, token: bytes) -> str:
    """Decrypt a token using the provided key."""
    fernet = Fernet(key)
    return fernet.decrypt(token).decode("utf-8")