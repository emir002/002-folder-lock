import os
import json
from main_lock import AccessControl
from crypto import load_password, save_password
from folder_path import read_path_file, write_path_file

def initial_setup():
	FOLDER_NAME = "002 Folder Lock"
	appdata_folder = os.path.join(os.getenv('APPDATA'), FOLDER_NAME)
	appdata_key_file = os.path.join(appdata_folder, "key.key")
	current_folder = os.path.abspath(os.path.dirname(__file__))
	password_filename = "password.json"
	password_file_path = os.path.join(current_folder, password_filename)
	attempts_file_path = os.path.join(appdata_folder, "attempts")

	max_attempts = 5  # Maximum allowed incorrect password attempts
	wrong_attempts = 0  # Initialize wrong password attempts counter

	if os.path.exists(appdata_key_file):
		if os.path.exists(password_file_path) and os.path.getsize(password_file_path) > 0:
			print("This is a command line tool to lock/unlock folders with a password in Windows.")
			
			# Load previous attempts from the file if it exists, or create a new one
			if os.path.exists(attempts_file_path):
				with open(attempts_file_path, "r") as attempts_file:
					wrong_attempts = int(attempts_file.read())
			else:
				with open(attempts_file_path, "w") as attempts_file:
					attempts_file.write("0")
			
			while wrong_attempts < max_attempts:
				check_password_input = input("Please enter the password to access: ").strip()
				stored_password = load_password()
				
				if check_password_input == stored_password:
					main()
					# Reset attempts count and update file
					wrong_attempts = 0
					with open(attempts_file_path, "w") as attempts_file:
						attempts_file.write("0")
					return stored_password
				else:
					wrong_attempts += 1
					remaining_attempts = max_attempts - wrong_attempts
					print(f"Incorrect password. {remaining_attempts} attempts remaining.")
	
				# Update the attempts count in the file
				with open(attempts_file_path, "w") as attempts_file:
					attempts_file.write(str(wrong_attempts))

			
			print("Maximum number of incorrect attempts reached. Access denied.")
			return None
		else:
			print("Something is wrong with the password file.")
			print("Please restore the original password file to the program folder.")
			print("The program will now quit.")
			print("----------------------------------------------------")
			quit()
	else:
		print("Welcome to the folder locking tool!")
		set_new_password()
		return None


# Function to set a new password for the folder locking tool
def set_new_password():
	print("It looks like you are using this tool for the first time.")
	new_password = input("Enter the new password: ")
	save_password(new_password)
	print("Password set successfully.")
	main()  # Continue to the main menu

# Function to change the password for the folder locking tool
def change_password():
	stored_password = load_password()
	if stored_password is not None:
		old_password = input("Enter the old password: ")
		if old_password == stored_password:
			new_password = input("Enter the new password: ")
			save_password(new_password)
			print("Password changed successfully.")
		else:
			print("Incorrect old password. Password change failed.")
	else:
		print("No password exists. Please set a new password.")
		set_new_password()
		
# Function to lock a folder using a password
def lock_folder_with_password(folder_path, password):
	locker = AccessControl(folder_path, password)
	try:
		locker.lock_folder_with_password(password)
		print("Folder locked successfully.")
	except Exception as e:
		print('Error occurred:', str(e))

# Function to unlock a folder using a password
def unlock_folder_with_password(folder_path, password):
	locker = AccessControl(folder_path, password)
	try:
		locker.unlock_folder_with_password(password)
		print("Folder unlocked successfully.")
	except Exception as e:
		print('Error occurred:', str(e))

# Function to check the status of a locked/unlocked folder and perform actions
def check_folder_status(folder_path, password):
    locker = AccessControl(folder_path, password)
    while True:
        try:
            if locker.is_folder_locked(password):
                print("Folder is currently locked.")
                action = input("Would you like to unlock the folder? (yes/no): ").lower()
                if action == "yes":
                    locker.unlock_folder_with_password(password)
                    break
                elif action == "no":
                    break  # Exit the loop and go back to the main menu
                else:
                    print("Please enter yes/no")
            else:
                print("Folder is currently unlocked.")
                action = input("Would you like to lock the folder? (yes/no): ").lower()
                if action == "yes":
                    locker.lock_folder_with_password(password)
                    break
                elif action == "no":
                    break  # Exit the loop and go back to the main menu
                else:
                    print("Please enter yes/no")
        except Exception as e:
            print('Error occurred:', str(e))
            break  # Exit the loop and go back to the main menu



# Function to check if a folder exists and is accessible
def folder_exists_and_accessible(path):
	try:
		return os.path.exists(path) and os.path.isdir(path) and os.access(path, os.R_OK)
	except Exception as e:
		return False

def get_folder_path(data):
	if 'folder_path' in data:
		print(f"This is the folder you used last time: {data['folder_path']}.")
		print("Is the path correct? yes/no or q to return to the main menu:")
		yes_no = input(">> ").lower()

		if yes_no == "yes":
			return data['folder_path']
		elif yes_no == "no":
			folder_path = input("Enter correct path >> ").strip()
			data['folder_path'] = folder_path
			write_path_file(data)
			print(" ")
			return folder_path
		else:
			return None
	else:
		print("Press q to quit")
		folder_path = input("Enter path >> ").strip()

		if folder_path == "q":
			return None
		else:
			data['folder_path'] = folder_path
			write_path_file(data)
			print(" ")
			return folder_path

def perform_lock_unlock_actions(folder_path, stored_password):
	while True:
		print("Choose action:")
		print("1. Lock the folder")
		print("2. Unlock the folder")
		action_choice = input("Enter your choice (1/2): ").strip()

		if action_choice == "1":
			lock_folder_with_password(folder_path, stored_password)
			break
		elif action_choice == "2":
			unlock_folder_with_password(folder_path, stored_password)
			break
		else:
			print("Invalid choice. Please select '1' to lock or '2' to unlock.")


def main():
	data = read_path_file()
	stored_password = load_password()

	while True:
		print("-----------------------------------------------")
		print("1. Check if the folder is locked/unlocked")
		print("2. Change the password")
		print("3. Lock/Unlock a folder")
		print("4. Quit")
		check_choice = input("Enter your choice (1/2/3/4): ").strip()
		print(" ")

		if check_choice == "1":
			folder_path = get_folder_path(data)
			if folder_path:
				if folder_exists_and_accessible(folder_path):
					check_folder_status(folder_path, stored_password)
				elif os.path.exists(folder_path):
					print("Folder is locked.")
				else:
					print("The folder does not exist.")
		elif check_choice == "2":
			change_password()
		elif check_choice == "3":
			folder_path = get_folder_path(data)
			if folder_path:
				perform_lock_unlock_actions(folder_path, stored_password)
		elif check_choice == "4":
			print("Thank you for using this tool")
			quit()
		else:
			print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
	initial_setup()
