import os
import win32security
import win32con
from crypto import encrypt_file, decrypt_file, load_key, get_key_path

class AccessControl:

    def __init__(self, folder_path, password):
        self.folder_path = folder_path
        self.password = password
        self.lock_file_path = os.path.join(self.folder_path, '.lock')
        self.key = load_key(get_key_path(os.getenv('APPDATA')))

    def lock_folder_with_password(self, password):
        try:
            # Encrypt files before locking
            self._encrypt_folder_contents()

            # Create a hidden lock file as an indicator of the locked state
            with open(self.lock_file_path, 'w') as lock_file:
                lock_file.write(password)
            # Deny access to everyone
            self._deny_access_to_everyone()

            print('Folder locked with password.')

        except Exception as e:
            print('Error occurred:', str(e))

    def unlock_folder_with_password(self, password):
        try:
            # Remove the hidden lock file to indicate the unlocked state
            if os.path.exists(self.lock_file_path):
                os.remove(self.lock_file_path)
            # Allow access to the authenticated users
            self._allow_access_to_authenticated_users()

            # Decrypt files after unlocking
            self._decrypt_folder_contents()

            print('Folder unlocked with password.')

        except Exception as e:
            print('Error occurred:', str(e))

    def is_folder_locked(self, password):
        try:
            # Check if the hidden lock file exists and contains the correct password
            if os.path.exists(self.lock_file_path):
                with open(self.lock_file_path, 'r') as lock_file:
                    stored_password = lock_file.read()
                return stored_password == password
            else:
                return False
        except Exception as e:
            print('Error occurred while checking folder lock status:', str(e))
            return False

    def _encrypt_folder_contents(self):
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):
                try:
                    encrypt_file(file_path, self.key)
                except Exception as e:
                    print(f'Error occurred while encrypting {file_path}:', str(e))


    def _decrypt_folder_contents(self):
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):
                try:
                    decrypt_file(file_path, self.key)
                except Exception as e:
                    print(f'Error occurred while encrypting {file_path}:', str(e))

    def _deny_access_to_everyone(self):
        try:
            acl = win32security.ACL()
            everyone_sid = win32security.ConvertStringSidToSid('S-1-1-0')
            acl.AddAccessDeniedAce(win32security.ACL_REVISION, win32con.GENERIC_READ | win32con.GENERIC_WRITE | win32con.GENERIC_EXECUTE, everyone_sid)
            sd = win32security.GetFileSecurity(self.folder_path, win32security.DACL_SECURITY_INFORMATION)
            sd.SetSecurityDescriptorDacl(1, acl, 0)
            win32security.SetFileSecurity(self.folder_path, win32security.DACL_SECURITY_INFORMATION, sd)
        except Exception as e:
            print('Error occurred while denying access to everyone:', str(e))

    def _allow_access_to_authenticated_users(self):
        try:
            acl = win32security.ACL()
            user_sid = win32security.LookupAccountName(None, 'Authenticated Users')[0]
            acl.AddAccessAllowedAce(win32security.ACL_REVISION, win32con.GENERIC_READ | win32con.GENERIC_WRITE | win32con.GENERIC_EXECUTE, user_sid)
            sd = win32security.GetFileSecurity(self.folder_path, win32security.DACL_SECURITY_INFORMATION)
            sd.SetSecurityDescriptorDacl(1, acl, 0)
            win32security.SetFileSecurity(self.folder_path, win32security.DACL_SECURITY_INFORMATION, sd)
        except Exception as e:
            print('Error occurred while allowing access to authenticated users:', str(e))
