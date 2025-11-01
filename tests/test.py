from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import sqlite3
import base64
import os


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
    conn = sqlite3.connect("data/test_vault.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
                   id INTEGER PRIMARY KEY,
                   website TEXT NOT NULL,
                   username TEXT NOT NULL,
                   password BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_password(website, username, password, key):
    encrypted = encrypt_passwords(key, password)
    conn = sqlite3.connect("data/test_vault.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO passwords (website, username, password)
                   VALUES (?, ?, ?)''',
                   (website, username, encrypted))
    conn.commit()
    conn.close()

def get_passwords(key):
    conn = sqlite3.connect("data/test_vault.db")
    cursor = conn.cursor()
    cursor.execute("SELECT website, username, password FROM passwords")
    for row in cursor.fetchall():
        website, username, encrypt_pw = row
        decrypted = decrypt_passwords(key, encrypt_pw)
        print(f"Website: {website} | Username: {username} | Password: {decrypted}")
    conn.close()

def load_or_create_salt():
    """Load the salt from a file or create a new one if it does not exist."""
    if not os.path.exists('salt.bin'):
        salt = os.urandom(16)
        with open('salt.bin', 'wb') as file:
            file.write(salt)

    else:
        with open('salt.bin', 'rb') as file:
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


        
