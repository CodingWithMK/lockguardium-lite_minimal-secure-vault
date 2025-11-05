from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import sqlite3
import base64
import os

DB_PATH = "data/test_vault.db"
SALT_PATH = "data/salt.bin"

def ensure_data_dir():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_key_from_password(password, salt):    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
        backend=default_backend()
    )

    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_passwords(key, password):
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def decrypt_passwords(key, token):
    fernet = Fernet(key)
    return fernet.decrypt(token).decode()

def create_db():
    """Init DB - uses context manager so connections always closed."""
    ensure_data_dir()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY,
                    website TEXT NOT NULL,
                    username BLOB NOT NULL,
                    password BLOB NOT NULL
            )
        ''')

        # optional: Small settings table for verifier token
        conn.commit()

def save_password(website, username, password, key):
    encrypted_username = encrypt_passwords(key, username)
    encrypted_pw = encrypt_passwords(key, password)
    ensure_data_dir()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO passwords (website, username, password)
                    VALUES (?, ?, ?)''',
                    (website, encrypted_username, encrypted_pw))
        conn.commit()

def get_passwords(key):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT website, username, password FROM passwords")
        for website, enc_user, enc_pw in cursor.fetchall():
            user = decrypt_passwords(key, enc_user)
            password = decrypt_passwords(key, enc_pw)
            print(f"Website: {website} | Username: {user} | Password: {password}")

def load_or_create_salt():
    """Load the salt from a file or create a new one if it does not exist."""
    ensure_data_dir()
    if not os.path.exists(SALT_PATH):
        salt = os.urandom(16)
        with open(SALT_PATH, 'wb') as file:
            file.write(salt)

    else:
        with open(SALT_PATH, 'rb') as file:
            salt = file.read()
    
    return salt


def main():
    salt = load_or_create_salt()

    master_password = input("Enter your master password: ")

    key = get_key_from_password(master_password, salt)

    while True:
        choice = input("1. Save Password\n2. View Passwords\n3. Exit\nChoose: ")
        
        if choice == "1":
            site = input("Website/App: ")
            user = input("Username/Email: ")
            pw = input("Password: ")
            save_password(site, user, pw, key)
        elif choice == "2":
            get_passwords(key)
        else:
            break

if __name__ == "__main__":
    create_db()
    main()


        
