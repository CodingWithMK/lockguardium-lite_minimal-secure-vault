import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple
from .models import PasswordEntry
from .crypto import encrypt_password, decrypt_password

class DatabaseManager:
    """
    Manages the local SQLite database for LockGuardium Lite.
    Combines data persistence with maximum protection against metadata leaks.
    """
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initializes the database schema if it does not already exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    website BLOB,
                    email BLOB,
                    username BLOB,
                    password BLOB
                );
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vault_config (
                    setting_key TEXT PRIMARY KEY,
                    setting_value BLOB
                );
            """)

    # --- CONFIG OPERATIONS (SALT & CANARY) ---

    def get_vault_config(self) -> Tuple[Optional[bytes], Optional[bytes]]:
        """
        Reads the salt and encrypted canary from the configuration vault.
        Returns a tuple of (salt, canary). If empty, returns (None, None).
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT setting_key, setting_value FROM vault_config WHERE setting_key IN ('salt', 'canary');"
            )
            rows = cursor.fetchall()
            
        config = {row[0]: row[1] for row in rows}
        return config.get("salt"), config.get("canary")

    def save_vault_config(self, salt: bytes, encrypted_canary: bytes):
        """Persists the salt and encrypted canary during the initial vault setup."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO vault_config (setting_key, setting_value) VALUES ('salt', ?);", 
                (salt,)
            )
            conn.execute(
                "INSERT OR REPLACE INTO vault_config (setting_key, setting_value) VALUES ('canary', ?);", 
                (encrypted_canary,)
            )

    # --- PASSWORD ENTRY OPERATIONS (CRUD) ---

    def save_password_entry(self, entry: PasswordEntry, key: bytes):
        """
        Accepts a validated PasswordEntry, encrypts all data fields using 
        the active session key, and persists the record into the database.
        """
        enc_website = encrypt_password(key, entry.website)
        enc_email = encrypt_password(key, entry.email)
        enc_username = encrypt_password(key, entry.username if entry.username else "")
        enc_password = encrypt_password(key, entry.password)

        query = "INSERT INTO passwords (website, email, username, password) VALUES (?, ?, ?, ?);"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query, (enc_website, enc_email, enc_username, enc_password))

    def get_all_entries(self, key: bytes) -> List[PasswordEntry]:
        """
        Retrieves all encrypted records, decrypts them in-memory using the session key, 
        and returns them as a list of validated PasswordEntry Pydantic models.
        """
        query = "SELECT website, email, username, password FROM passwords;"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()

        decrypted_entries = []
        for row in rows:
            dec_website = decrypt_password(key, row[0])
            dec_email = decrypt_password(key, row[1])
            dec_username = decrypt_password(key, row[2])
            dec_password = decrypt_password(key, row[3])

            entry = PasswordEntry(
                website=dec_website,
                email=dec_email,
                username=dec_username,
                password=dec_password
            )
            decrypted_entries.append(entry)

        return decrypted_entries