import os, base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_PATH = "salt.bin"
ITERATIONS = 600_000
CANARY_PLAINTEXT = "LOCKGUARDIUM_VAULT_VALIDATED"

def generate_new_salt() -> bytes:
    """Generates a secure 16-byte salt (CSPRNG)."""
    return os.urandom(16)

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a key from the password and salt using PBKDF2."""
    pwd = password.encode("utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
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

def verify_master_password(key: bytes, encrypted_canary: bytes) -> bool:
    """
    Verifies the canary value to check if the master password is correct.
    Returns True if password is correctly derived, False otherwise raising an InvalidToken.
    """
    try:
        decrypted = decrypt_password(key, encrypted_canary)
        return decrypted == CANARY_PLAINTEXT
    except InvalidToken:
        return False