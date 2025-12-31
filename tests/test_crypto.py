import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordManager:
    def __init__(self, master_password):
        """Initializing initial dependencies and master password."""
        self.key = self._generate_key(master_password)
        self.cipher = Fernet(self.key)
        self.storage_file = "passwords.enc"
        self.passwords = {}

        # Loading existing passwords if file exists
        if os.path.exists(self.storage):
            self.load_passwords()

    def ensure_data_dir(self, DB_PATH = "data/test_vault.db"):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    def _generate_key(self, master_password, salt):
        """Generate encryption key from master password."""   # In real use case, never store on device.
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=200000
        )
        key = base64.urlsafe_b64decode(kdf.derive(master_password.encode()))
        return key
    
    def add_password(self, website, username, password):
        """Add or update a password entry"""
        self.passwords[website] = {
            'username': username,
            'password': password
        }
        self.save_passwords()

    def get_password(self, website):
        """Retrieve a password entry"""
        if website in self.passwords:
            return self.passwords[website]
        return None

    def delete_password(self, website):
        """Remove a password entry."""
        if website in self.passwords:
            del self.passwords[website]
            self.save_passwords()
        return False
    
    def get_all_websites(self):
        """Return all stored webiste names"""
        return list(self.passwords.keys())
    
    def save_passwords(self):
        """Encrypt and save passwords to file."""
        encrypted_data = self.cipher.encrypt(json.dumps(self.passwords).encode())
        with open(self.storage_file, "wb") as file:
            file.write(encrypted_data)

    def load_passwords(self):
        """Decrypt and load passwords from file."""
        try:
            with open(self.storage_file, "rb") as file:
                encrypted_data = file.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                self.passwords = json.loads(decrypted_data)
        except Exception as e:
            print(f"Error loading passwords: {e}")
            self.passwords = {}

    def load_or_create_salt(self, SALT_PATH = "data/salt.bin"):
        """Load the salt from a file or create a new one if it does not exist."""
        self.ensure_data_dir()
        if not os.path.exists(SALT_PATH):
            salt = os.urandom(16)
            with open(SALT_PATH, 'wb') as file:
                file.write(salt)

        else:
            with open(SALT_PATH, 'rb') as file:
                salt = file.read()
        
        return salt

    def verify_master_pass(self, master_password):
        """Verify if the provided master password is correct."""
        test_key = self._generate_key(master_password)
        return test_key == self.key

        