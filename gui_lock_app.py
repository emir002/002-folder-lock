import os
import json
from main_lock import AccessControl
from crypto import load_password, save_password
from folder_path import read_path_file, write_path_file

class FolderLockManager:
    def __init__(self):
        # Initial setup for folder lock manager, defining paths and file names
        self.FOLDER_NAME = "002 Folder Lock"
        self.appdata_folder = os.path.join(os.getenv('APPDATA'), self.FOLDER_NAME)
        self.appdata_key_file = os.path.join(self.appdata_folder, "key.key")
        self.current_folder = os.path.abspath(os.path.dirname(__file__))
        self.password_filename = "password.json"
        self.password_file_path = os.path.join(self.current_folder, self.password_filename)
        self.attempts_file_path = os.path.join(self.appdata_folder, "attempts")
        self.max_attempts = 5  # Max attempts for password entry

    def check_initial_setup(self):
        # Checks the initial setup status
        if not os.path.exists(self.appdata_key_file):
            return "setup_required"
        elif not (os.path.exists(self.password_file_path) and os.path.getsize(self.password_file_path) > 0):
            return "password_file_error"
        else:
            return "enter_password"

    def verify_password(self, input_password):
        # Verifies input password against the stored one
        wrong_attempts = self.read_wrong_attempts()
        if wrong_attempts >= self.max_attempts:
            raise Exception("Maximum number of incorrect attempts reached. Access denied.")

        stored_password = load_password()
        if input_password == stored_password:
            self.reset_wrong_attempts()
            return True
        else:
            self.increment_wrong_attempts()
            remaining_attempts = self.max_attempts - self.read_wrong_attempts()


    def set_new_password(self, new_password):
        # Sets a new password
        save_password(new_password)

    def change_password(self, old_password, new_password):
        # Changes the password after verifying the old one
        stored_password = load_password()
        if old_password == stored_password:
            save_password(new_password)
            return True
        else:
            return False

    def read_wrong_attempts(self):
        # Reads the number of wrong password attempts from a file
        if os.path.exists(self.attempts_file_path):
            with open(self.attempts_file_path, "r") as attempts_file:
                return int(attempts_file.read())
        else:
            return 0

    def reset_wrong_attempts(self):
        # Resets the wrong password attempts count
        with open(self.attempts_file_path, "w") as attempts_file:
            attempts_file.write("0")

    def increment_wrong_attempts(self):
        # Increments the wrong password attempts count
        wrong_attempts = self.read_wrong_attempts() + 1
        with open(self.attempts_file_path, "w") as attempts_file:
            attempts_file.write(str(wrong_attempts))
    
    def lock_folder_with_password(self, folder_path, password):
        # Locks a folder with the provided password
        locker = AccessControl(folder_path, password)
        try:
            locker.lock_folder_with_password(password)
            return True
        except Exception as e:
            raise Exception(f'Error occurred while locking the folder: {str(e)}')

    def unlock_folder_with_password(self, folder_path, password):
        # Unlocks a folder with the provided password
        locker = AccessControl(folder_path, password)
        try:
            locker.unlock_folder_with_password(password)
            return True
        except Exception as e:
            raise Exception(f'Error occurred while unlocking the folder: {str(e)}')

    def check_and_manage_folder_status(self, folder_path, password):
        locker = AccessControl(folder_path, password)
        try:
            if locker.is_folder_locked(password):
                return "locked"
            else:
                return "unlocked"
        except Exception as e:
            raise Exception(f'Error occurred while checking folder status: {str(e)}')

    def folder_exists_and_accessible(self, path):
        # Checks if a folder exists and is accessible
        try:
            if os.path.exists(path) and os.path.isdir(path) and os.access(path, os.R_OK):
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f'Error checking if folder exists and is accessible: {str(e)}')

    def get_folder_path(self):
        # Adjusted to read directly from the 'path.json' file
        try:
            with open('path.json', 'r') as file:
                data = json.load(file)
                return ("existing", data.get('folder_path', None)) if 'folder_path' in data else ("none", None)
        except (FileNotFoundError, json.JSONDecodeError):
            return ("none", None)

    def update_folder_path(self, data, new_path):
        # Updates the folder path in the data and writes it to a file
        data['folder_path'] = new_path
        write_path_file(data)
        return new_path
