import os
from cryptography.fernet import Fernet
from pathlib import Path

# Constants for file paths and folder names
PASSWORD_FILE = "pas1.json"
KEY_FILE = "key.key"
KEY_FILE_1 = "key1.key"  # New key file name
FOLDER_NAME = "002 Folder Lock"  # Folder name for key file
FOLDER_NAME1 = "Vlc1"  # Folder name for password file

def generate_key(key_path):
    """
    Generates a new encryption key and saves it to the specified path.
    """
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)

def load_key(key_path):
    """
    Loads an encryption key from the specified path. If the key file does not
    exist, it generates a new key file at that path.
    """
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            return key_file.read()
    else:
        generate_key(key_path)
        return load_key(key_path)

def create_folder_if_not_exists(folder_path):
    """
    Creates a folder at the specified path if it does not already exist.
    """
    Path(folder_path).mkdir(parents=True, exist_ok=True)

def get_key_path():
    """
    Returns the file path for the original key file.
    """
    key_folder_path = os.path.join(os.getenv('APPDATA'), FOLDER_NAME)
    create_folder_if_not_exists(key_folder_path)
    return os.path.join(key_folder_path, KEY_FILE)

def get_key1_path():
    """
    Returns the file path for the additional key file 'key1.key'.
    """
    key_folder_path = os.path.join(os.getenv('APPDATA'), FOLDER_NAME)
    create_folder_if_not_exists(key_folder_path)
    return os.path.join(key_folder_path, KEY_FILE_1)

# Encryption and decryption functions

def encrypt_password(password, key):
    """
    Encrypts the provided password using the provided key.
    """
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    """
    Decrypts the provided encrypted password using the provided key.
    """
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

def encrypt_file(file_path, key):
    """
    Encrypts the file at the given file path using the provided key.
    """
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(file_path, key):
    """
    Decrypts the file at the given file path using the provided key.
    """
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

# Password handling functions

def load_password():
    """
    Loads and decrypts the password from the password file.
    """
    appdata_folder = os.path.join(os.getenv('APPDATA'), FOLDER_NAME1)
    password_file_path = os.path.join(appdata_folder, PASSWORD_FILE)
    appdata_key_path = get_key_path()
    
    if os.path.exists(password_file_path):
        with open(password_file_path, "rb") as file:
            encrypted_password = file.read().strip()
            key = load_key(appdata_key_path)
            return decrypt_password(encrypted_password, key)
    else:
        return None

def save_password(password):
    """
    Encrypts and saves the password to the password file.
    """
    appdata_folder = os.path.join(os.getenv('APPDATA'), FOLDER_NAME1)
    create_folder_if_not_exists(appdata_folder)
    
    password_file_path = os.path.join(appdata_folder, PASSWORD_FILE)
    appdata_key_path = get_key_path()
    
    key = load_key(appdata_key_path)
    encrypted_password = encrypt_password(password, key)
    with open(password_file_path, "wb") as file:
        file.write(encrypted_password)

# Modified functions to use key1.key

def encrypt_dax_file(file_path, key=None):
    """
    Encrypts the specified file using 'key1.key'. If the key is not provided,
    it loads the key from 'key1.key'.
    """
    if key is None:
        key = load_key(get_key1_path())
    encrypt_file(file_path, key)

def decrypt_dax_file(file_path, key=None):
    """
    Decrypts the specified file using 'key1.key'. If the key is not provided,
    it loads the key from 'key1.key'.
    """
    if key is None:
        key = load_key(get_key1_path())
    decrypt_file(file_path, key)
