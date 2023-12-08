import os
from cryptography.fernet import Fernet
from pathlib import Path

PASSWORD_FILE = "password.json"
KEY_FILE = "key.key"
FOLDER_NAME = "002 Folder Lock"

def generate_key(key_path):
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)

def load_key(key_path):
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            return key_file.read()
    else:
        generate_key(key_path)
        return load_key(key_path)

def create_folder_if_not_exists(folder_path):
    Path(folder_path).mkdir(parents=True, exist_ok=True)

def get_key_path(folder_path):
    return os.path.join(folder_path, KEY_FILE)

def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

def load_password():
    appdata_folder = os.path.join(os.getenv('APPDATA'), FOLDER_NAME)
    appdata_key_path = get_key_path(appdata_folder)
    
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "rb") as file:
            encrypted_password = file.read().strip()
            key = load_key(appdata_key_path)
            return decrypt_password(encrypted_password, key)
    else:
        return None

def save_password(password):
    appdata_folder = os.path.join(os.getenv('APPDATA'), FOLDER_NAME)
    create_folder_if_not_exists(appdata_folder)
    
    appdata_key_path = get_key_path(appdata_folder)
    
    key = load_key(appdata_key_path)
    encrypted_password = encrypt_password(password, key)
    with open(PASSWORD_FILE, "wb") as file:
        file.write(encrypted_password)
