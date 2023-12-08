import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMenuBar, QFileDialog, QColorDialog,
                             QToolButton, QMessageBox, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QColor, QAction
from gui_lock_app import FolderLockManager
from main_lock import AccessControl
from crypto import load_password

current_folder = os.getcwd()
file_name = 'GUI readme.md'
help_file_path = os.path.join(current_folder, file_name)

class EnterPassWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.folder_lock_manager = FolderLockManager()
        
        # Set up the main window
        self.setWindowTitle("002 Folder Lock")
        self.setGeometry(100, 100, 400, 100)  # x, y, width, height
        self.setFixedSize(550, 120)

        # Create layout
        layout = QVBoxLayout()
        
        # Welcome label
        self.welcome_label = QLabel("Welcome to 002 Folder Lock")
        layout.addWidget(self.welcome_label)

        # Information label
        self.info_label = QLabel()
        layout.addWidget(self.info_label)

        # Password input section
        self.password_label = QLabel("Enter Password:")
        self.password_input = QLineEdit()
        
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.eye_button = QToolButton()
        self.eye_button.setIcon(QIcon("eye.png"))  # Replace with the path to your eye icon
        self.eye_button.clicked.connect(self.toggle_password_visibility)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.password_label)
        h_layout.addWidget(self.password_input)
        h_layout.addWidget(self.eye_button)

        # Buttons and password attempt status
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.on_ok_button_clicked)
        self.cancel_button = QPushButton("Exit")
        self.cancel_button.clicked.connect(self.close)
        self.attempts_label = QLabel("Attempts Left")  # Renamed QLabel
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.attempts_label)  # Add the new label to the layout
        button_layout.addStretch()  # This will push the buttons to the right
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        self.update_attempts_label()  # Call the update method

        # Adding layouts
        layout.addLayout(h_layout)
        layout.addLayout(button_layout)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.setWindowIcon(QIcon('icon-5355895_1280.ico'))

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            

    def update_attempts_label(self):  # attempts label
        wrong_attempts = self.folder_lock_manager.read_wrong_attempts()
        self.attempts_label.setText(f"You can enter the password a maximum of five times. Attempt {wrong_attempts} of 5!")
        if wrong_attempts >= self.folder_lock_manager.max_attempts:
            self.password_input.setEnabled(False)
            self.attempts_label.setText(f"You had 5 of 5 wrong attempts. Application is locked")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.on_ok_button_clicked()
    
    def on_ok_button_clicked(self):
        # Get the password from QLineEdit
        entered_password = self.password_input.text()

        # Call the verify_password method and handle the result
        try:
            if self.folder_lock_manager.verify_password(entered_password):
                self.close()
                self.main_window = MainWindow()
                self.main_window.show()
            else:
                QMessageBox.warning(self, "Warning", "Incorrect password.")
                self.password_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            # Handle what should happen after too many wrong attempts
            self.folder_lock_manager.increment_wrong_attempts()
        finally:
            # Update the attempts label in both success and failure cases
            self.update_attempts_label()

class MainWindow(QMainWindow):
    def __init__(self):
        
        # Initialize a member to hold the window change_password_window
        # because it was garbage collected and window closes fraction of
        # second after it was opened and coffe_window was raising error
        # AttributeError: 'MainWindow' object has no attribute 'coffee_window'
        self.change_password_window = None
        self.coffee_window = None
        self.about_window = None
        
        super().__init__()
        self.folder_lock_manager = FolderLockManager()
        
        self.setWindowIcon(QIcon('icon-5355895_1280.ico'))


        self.setWindowTitle("002 Folder Lock")
        self.setGeometry(100, 100, 600, 140)
        self.setFixedSize(600, 140)
        
       # Creating menu bar
        menu_bar = self.menuBar()

        # Create the 'Options' menu
        options_menu = menu_bar.addMenu("Options")

        # Create and add 'Change Password' action to the 'Options' menu
        change_password_action = QAction("Change Password", self)
        change_password_action.triggered.connect(self.change_password)
        options_menu.addAction(change_password_action)

        # Add other actions to the 'Options' menu
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.help1)
        options_menu.addAction(help_action)
        
        cofee_action = QAction("Buy me a coffee", self)
        cofee_action.triggered.connect(self.coffee)
        options_menu.addAction(cofee_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        options_menu.addAction(about_action)

        # Creating main layout
        self.main_layout = QVBoxLayout()

        # Folder path section
        folder_path_layout = QHBoxLayout()
        folder_path_label = QLabel("Folder path:")
        self.folder_path_edit = QLineEdit()
        change_folder_btn = QPushButton("Change Folder")
        change_folder_btn.clicked.connect(self.change_folder)

        folder_path_layout.addWidget(folder_path_label)
        folder_path_layout.addWidget(self.folder_path_edit)
        folder_path_layout.addWidget(change_folder_btn)
        self.main_layout.addLayout(folder_path_layout)

        # Warning label
        warning_label = QLabel("Before locking double confirm that folder path is correct")
        warning_label.setStyleSheet("color: red;")
        self.main_layout.addWidget(warning_label)

        # Current folder status
        status_layout = QHBoxLayout()
        current_status_label = QLabel("Current folder status :")
        self.unlocked_label = QLabel("Unlocked")
        self.locked_label = QLabel("Locked")
        self.unlocked_label.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        self.locked_label.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        self.unlocked_label.setStyleSheet("color: blue;")
        self.locked_label.setStyleSheet("color: red;")

        status_layout.addWidget(current_status_label)
        status_layout.addWidget(self.unlocked_label)
        status_layout.addWidget(self.locked_label)
        self.main_layout.addLayout(status_layout)

        # Buttons for locking, unlocking, and exit
        self.button_layout = QHBoxLayout()
        self.unlock_button = QPushButton("Unlock folder")
        self.lock_button = QPushButton("Lock folder")
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        self.lock_button.clicked.connect(self.lock_folder)
        self.unlock_button.clicked.connect(self.unlock_folder)

        self.button_layout.addWidget(self.unlock_button)
        self.button_layout.addWidget(self.lock_button)
        self.button_layout.addWidget(self.exit_button)
        self.main_layout.addLayout(self.button_layout)

        # Set the central widget and its layout
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)
        
        # Load the last used folder path
        folder_path_status, folder_path = self.folder_lock_manager.get_folder_path()
        if folder_path_status == "existing":
            self.folder_path_edit.setText(folder_path)
            self.update_folder_status(folder_path)
        else:
            self.folder_path_edit.setText("")
            self.update_ui_based_on_path()
        

    def change_folder(self):
        desktop_path = os.path.expanduser("~/Desktop")
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", desktop_path)
        if folder_path:
            self.folder_path_edit.setText(folder_path)
            accessible = self.folder_lock_manager.folder_exists_and_accessible(folder_path)
            if not accessible:
                QMessageBox.information(self, "Information", "The folder does not exist or is not available. Please select another folder.")
            else:
                self.update_folder_status(folder_path)

    def update_ui_based_on_path(self):
        path = self.folder_path_edit.text().strip()
        if path:
            # Enable labels and buttons as a default state
            self.unlocked_label.setEnabled(True)
            self.locked_label.setEnabled(True)
            self.lock_button.setEnabled(True)
            self.unlock_button.setEnabled(True)
        else:
            # Disable and gray out labels and buttons
            self.unlocked_label.setDisabled(True)
            self.locked_label.setDisabled(True)
            self.lock_button.setDisabled(True)
            self.unlock_button.setDisabled(True)


    #If folder is already locked gray out lock button and vice version
    def update_folder_status(self, folder_path):
        pass1 = load_password()
        locker = AccessControl(folder_path, pass1)
        try:
            if locker.is_folder_locked(pass1):
                self.unlocked_label.setStyleSheet("color: transparent;")
                self.locked_label.setStyleSheet("color: red;")
                self.lock_button.setDisabled(True)
                self.unlock_button.setEnabled(True)
            else:
                self.locked_label.setStyleSheet("color: transparent;")
                self.unlocked_label.setStyleSheet("color: blue;")
                self.unlock_button.setDisabled(True)
                self.lock_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def lock_folder(self):
        pass2 = load_password()
        locker = FolderLockManager()
        folder_path = self.folder_path_edit.text().strip()
        try:
            locker.lock_folder_with_password(folder_path, pass2)
            self.update_folder_status(folder_path)
            self.update_path()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def unlock_folder(self):
        pass2 = load_password()
        locker = FolderLockManager()
        folder_path = self.folder_path_edit.text().strip()
        try:
            locker.unlock_folder_with_password(folder_path, pass2)
            self.update_folder_status(folder_path)
            self.update_path()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_path(self):
        # Retrieve the new folder path from a text field or other input widget
        new_folder_path = self.folder_path_edit.text().strip()
        # Create an instance of FolderLockManager
        folder_lock_manager = FolderLockManager()
        # Update the folder path
        try:
            # Pass an empty dictionary as the current data, assuming FolderLockManager handles it
            folder_lock_manager.update_folder_path({}, new_folder_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def change_password(self):
        if not self.change_password_window:
            self.change_password_window = ChangePassword()
        self.change_password_window.show()
    
    def help1(self):
        try:
            subprocess.Popen(['notepad.exe', help_file_path])
        except FileNotFoundError:
            QMessageBox.critical(self, "Readme file not found", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def coffee(self):
        if not self.coffee_window:
            self.coffee_window = Coffee()
        self.coffee_window.show()
        
    def about(self):
        if not self.about_window:
            self.about_window = About()
        self.about_window.show()
    
class FirstTimeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.folder_lock_manager = FolderLockManager()
        
        self.main_window = FirstTimeWindow
        
        self.setWindowTitle("Welcome!")
        self.setGeometry(100, 100, 480, 180)  # x, y, width, height
        self.setFixedSize(480, 180)
        self.setWindowIcon(QIcon('icon-5355895_1280.ico'))

        # Create main layout
        layout = QVBoxLayout()

        # Labels
        layout.addWidget(QLabel("You are using the app for the first time."))
        layout.addWidget(QLabel("Please enter a new password."))
        warning_label = QLabel("Please write down or remember the password because it is not possible to recover it!")
        warning_label.setStyleSheet("color: red;")
        layout.addWidget(warning_label)

        # Password input field with label
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Input password:   "))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_input, 1)

        # Password visibility toggle
        self.eye_button = QToolButton()
        self.eye_button.setIcon(QIcon("eye.png"))  # Replace with the path to your eye icon
        self.eye_button.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.eye_button)
        layout.addLayout(password_layout)

        # Repeat password input field with label
        repeat_password_layout = QHBoxLayout()
        repeat_password_layout.addWidget(QLabel("Repeat password:"))
        self.repeat_password_input = QLineEdit()
        self.repeat_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        repeat_password_layout.addWidget(self.repeat_password_input)
        layout.addLayout(repeat_password_layout, 1)

        # OK and Exit buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.on_ok_button_clicked)
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(exit_button)
        layout.addLayout(button_layout)

        # Set the central widget and its layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.repeat_password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.repeat_password_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def on_ok_button_clicked(self):
        entered_password = self.password_input.text()
        repeated_password = self.repeat_password_input.text()

        if entered_password == repeated_password and entered_password != "":
            self.folder_lock_manager.set_new_password(entered_password)
            QMessageBox.information(self, "Information", "New password set!")
            self.close()
            # Launch MainWindow after successful setup
            self.main_window = MainWindow()
            self.main_window.show()
        else:
            QMessageBox.information(self, "Information", "Passwords do not match, and password fields cannot be left empty.")

class ChangePassword(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.folder_lock_manager = FolderLockManager()
        
        self.setWindowTitle("Change password")
        self.setGeometry(100, 100, 480, 180)  # x, y, width, height
        self.setFixedSize(480, 180)
        self.setWindowIcon(QIcon('icon-5355895_1280.ico'))

        # Create main layout
        layout = QVBoxLayout()

        # Labels
        layout.addWidget(QLabel("Please enter a new password."))
        warning_label = QLabel("Please write down or remember the password because it is not possible to recover it!")
        warning_label.setStyleSheet("color: red;")
        layout.addWidget(warning_label)

        # Old Password input field with label
        old_password_layout = QHBoxLayout()
        old_password_layout.addWidget(QLabel("Old password:             "))
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        old_password_layout.addWidget(self.old_password_input)

        # Eye button for the old password visibility toggle
        self.eye_button = QToolButton()
        self.eye_button.setIcon(QIcon("eye.png"))  # Replace with the path to your eye icon
        self.eye_button.clicked.connect(self.toggle_password_visibility)
        old_password_layout.addWidget(self.eye_button)
        layout.addLayout(old_password_layout)

        # New Password input field with label
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Input new password:   "))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_input, 1)
        layout.addLayout(password_layout)

        # Repeat New Password input field with label
        repeat_password_layout = QHBoxLayout()
        repeat_password_layout.addWidget(QLabel("Repeat new password:"))
        self.repeat_password_input = QLineEdit()
        self.repeat_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        repeat_password_layout.addWidget(self.repeat_password_input)
        layout.addLayout(repeat_password_layout, 1)

        # OK and Exit buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.on_ok_button_clicked)
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(exit_button)
        layout.addLayout(button_layout)

        # Set the central widget and its layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def toggle_password_visibility(self):
        # Toggle visibility for both old and new password fields
        if self.old_password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.old_password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.repeat_password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.old_password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.repeat_password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def on_ok_button_clicked(self):
        # Get the passwords from QLineEdit
        old_pass = self.old_password_input.text()
        new_pass1 = self.password_input.text()
        new_pass2 = self.repeat_password_input.text()
        
        try:
            if old_pass == "" or new_pass1 == "" or new_pass2 == "":
                QMessageBox.warning(self, "Warning", "Password fields cannot be blank.")
                self.old_password_input.clear()
                self.password_input.clear()
                self.repeat_password_input.clear()
                self.old_password_input.setFocus()
            else:
                if new_pass1 == new_pass2:
                    success = self.folder_lock_manager.change_password(old_pass, new_pass1)
                    if success:
                        QMessageBox.information(self, "Password", "Password changed successfully.")
                        self.close()
                    else:
                        QMessageBox.warning(self, "Warning", "Incorrect old password.")
                        self.old_password_input.clear()
                        self.old_password_input.setFocus()
                else:
                    QMessageBox.warning(self, "Warning", "Entered new passwords must be the same.")
                    self.password_input.clear()
                    self.repeat_password_input.clear()
                    self.password_input.setFocus()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Window")
        self.setGeometry(100, 100, 600, 400)
        self.setFixedSize(800, 250)
        self.setWindowIcon(QIcon('icon-5355895_1280.ico'))

        # Define the label texts
        label_texts = [
            "If my tool has helped you or you use it in your business every day, I would appreciate it if you buy me a coffee:",
            "Paypal: net_hr@outlook.com",
            "Monero: 49D8Vbe2cpsiWxHhgjfExz2NECvdoaZhoJS33gaiUbPhY2PJZQuQfsbhR7pyGsxaEP4UkPhiWz6kCc9j7YzVs1psTMHxo4G",
            "Ethereum: 0x33234686d42eb8b2f96f75f061bc01a302515014",
            "Ethereum Classic: 0x33234686d42eb8b2f96f75f061bc01a302515014",
            "Avalanche AVAX: 0xEEcc1d4c922b66C174600455290ddfAA9f07c73F",
            "Thank you!"
        ]

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.button_label_map = {}  # Dictionary to map buttons to their corresponding labels

        for i in range(7):
            horizontal_layout = QHBoxLayout()

            label = QLabel(label_texts[i])
            if i == 0 or i == 6:
                label.setStyleSheet("font-weight: bold;")
            horizontal_layout.addWidget(label)

            if 1 <= i <= 5:
                copy_button = QPushButton("Copy")
                copy_button.setFixedSize(QSize(100, 25))
                horizontal_layout.addWidget(copy_button)

                self.button_label_map[copy_button] = label  # Map the button to the label
                copy_button.clicked.connect(self.copy_label_text)

            layout.addLayout(horizontal_layout)

        ok_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        ok_layout.addItem(spacer)

        ok_button = QPushButton("OK")
        ok_button.setFixedSize(QSize(100, 30))
        ok_button.clicked.connect(self.close)
        ok_layout.addWidget(ok_button)

        layout.addLayout(ok_layout)
        central_widget.setLayout(layout)

    def copy_label_text(self):
        sender = self.sender()
        label = self.button_label_map.get(sender)
        if label:
            text = label.text().split(":")[1].strip() if ':' in label.text() else label.text()
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

class About(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        self.setGeometry(100, 100, 300, 200)
        self.setFixedSize(300, 150)
        self.setWindowIcon(QIcon('icon-5355895_1280.ico'))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("You can reach me via mail :"))

        # Email label
        email_label = QLabel()
        email_label.setText('<a href="mailto:emir002@yahoo.com" style="color: blue; text-decoration: underline;">emir002@yahoo.com</a>')
        email_label.setOpenExternalLinks(True)  # Opens the link in the default mail client
        layout.addWidget(email_label)
        
        layout.addWidget(QLabel("or view source code of this program at :"))

        # GitHub URL label
        github_label = QLabel()
        github_label.setText('<a href="https://github.com/emir002" style="color: blue; text-decoration: underline;">https://github.com/emir002</a>')
        github_label.setOpenExternalLinks(True)  # Opens the link in the default web browser
        layout.addWidget(github_label)

        ok_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        ok_layout.addItem(spacer)

        ok_button = QPushButton("OK")
        ok_button.setFixedSize(QSize(100, 30))
        ok_button.clicked.connect(self.close)
        ok_layout.addWidget(ok_button)

        layout.addLayout(ok_layout)
        central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    folder_lock_manager = FolderLockManager()
    first_setup = folder_lock_manager.check_initial_setup()

    if first_setup == "setup_required":
        # Directly open the FirstTimeWindow for first-time setup
        window = FirstTimeWindow()
        
    elif first_setup == "password_file_error":
        QMessageBox.critical(None, "Warning", "Something is wrong with the password file. App will now quit.")
        sys.exit(0)  # Quit the application
    else:
        # Proceed with opening the EnterPassWindow
        window = EnterPassWindow()

    window.show()
    sys.exit(app.exec())
