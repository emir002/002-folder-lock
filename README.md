# 002 Folder Lock  

## Summary
002 Folder lock is a tool for simply locking folders in the Windows system with a password. Locked folders cannot be accessed from Windows, they cannot be deleted or copied. You can download the compiled version of the tool ready for installation [HERE](link goes here).
002 Folder Lock works by modifying windows security descriptors at the folder level. You can read about them here: [windows security descriptors.](https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptors)
**Note:** Never store important passwords or credit card numbers in a locked folder! 002 Folder Lock prohibits access to the folder from the windows platform only. The files in the locked folder are encrypted using using the Fernet symmetric encryption provided by the cryptography library in Python. While Fernet provides strong encryption, the security of the encrypted data also heavily depends on the security of the key. If the key is compromised, the encryption can be easily broken. The program is designed for simplicity and speed of use, not for ultimate security. If you want security as much as Windows can provide save your key to USB drive or another location physically separated from the computer.  

## Overview
File cmd_lock_app represents the main logic of the program as well as the user interface. When starting the program for the first time, it checks whether there is an encryption key in '%APPDATA%\002 Folder Lock', and if the encryption key is not present, it will generate a new key and ask to set a new password. The encrypted password is in the password.json file located in the current folder. If the password.json file does not exist or if the encrypted code has been changed, the program will be locked permanently and will inform the user to restore the original password.json file. The user has the right to enter the wrong code 5 times before the program is locked. The number of attempts to enter correct password is saved into a 'file' located in the folder '%APPDATA%\002 Folder Lock'  

## False positive  
Some antivirus software (such as Avira - tested) falsely report the program after installation as positive for Trojans / ransomware due to encryption modules and block the program from starting. If this happens restore program from antivirus quarantine, add it to the whitelist of the antivirus program and continue using it normally. For your own safety, you can upload the program to one of the online programs for checking the presence of viruses, such as: https://www.eset.com/int/home/online-scanner/ or https://opentip.kaspersky.com

## Speed
The speed of encryption/decryption depends on the speed of your processor and SSD/HDD disk. For larger files and a larger number of files, use the command line version because it is faster than the GUI version.  

## Increasing security
The default locations for the files are: \AppData\Roaming\002 Folder Lock\attempts - for the number of password attempts and \AppData\Roaming\002 Folder Lock\key.key for the encryption key. The second folder where the password for the folder is located is AppData\Roaming\Vlc1\pas1.json where the encrypted password is located. Moving the Vlc1 folder to the USB stick will permanently lock the program until the original folder is returned to its original location. Moving the Vlc1 and 002 Folder Lock folders to the USB stick will reset the program to its original settings and the program will ask the user to reset the password. All locked folders will be unlocked, however, all files locked with the old password will not be readable, because the program sets a new random encryption key at each initialization. By returning the original Vlc1 and 002 Folder Lock folders to their original locations, the user will be able to unlock and properly access the originally locked folders and files.

Conclusion: for maximum possible security, cut the Vlc1 folder from the \AppData\Roaming\ folder and paste it on the USB stick. To unlock the program again, return the Vlc1 folder to its original location.

## Manifest file
This app uses manifest file which gives it administrator rights so it can change the files in it default installation folder which is C:\Program Files (x86)\002 Folder Lock. This was done due to the greater resistance of the app from changes, locking by antivirus software, deletion, etc. If the user does not have administrator access, the application will have to be installed outside the "Program Files" folder to work normally.  

## Functions (cmd version)
When the user accesses the program, he has the following options:  
1. Check if the folder is locked/unlocked  
2. Change the password  
3. Lock/Unlock a folder  
4. Quit  

The first option will ask the user if the last entered folder path is correct. The path to the last locked/unlocked file is saved in 'path.json' file in current folder. If the user confirms, the program will check whether the desired folder is locked or unlocked and will ask if the user wants to lock or unlock the folder. The program determines the status of the folder (unlocked/locked) by placing a '.lock' file in the folder when it is locked. When checking whether the file is unlocked or locked, the program will first unlock the folder, check whether the '.lock' file exists inside, lock the folder again if it find '.lock' file inside and return the status of the folder.  

The second option allows changing the access code. The user must first enter the old password to set a new one.  

The third option first asks the user to confirm if the last folder that was unlocked/locked is the correct folder. The path to the last locked/unlocked file is saved in the 'path.json' file in the current folder. If the user confirms, he has two options: 1. to lock the folder and 2. to unlock the folder  

The fourth option exits the program  

A detailed view of classes and functions is available in the files in 'docs' folder .html files are made with the pdoc3 module  

## Files

\'%APPDATA%'
|- \002 Folder Lock\attempts'	File that store number of wrong password imputs. It will be created after running the program.  
|- \002 Folder Lock\key.key'	File that store key for encrypting password. It will be created after running the program.  
|- \Vlc1\pas1.json'	Encrypted password file.  

\'002 Folder Lock'  
|     |-\'docs'  
|           |-\'cmd_lock_app.html'  
|           |-\'crypto.html'  
|           |-\'folder_path.html'  
|           |-\'gui_lock_app.html'  
|           |-\'main_lock.html'  
|           |-\'startwindows.html' 	GUI version  
|
|- 'cmd_lock_app.py'	Main logic of tool and command line user interface  
|- 'crypto.py'		Module that load/save, encrypt/decrypt password. This module save data to 'password.json'.  
|- 'dependencies.txt'	List of dependencies  
|- 'eye.png	'	icon in gui app  
|- 'folder_path.py'	Module that save/load locked folder path. This module save data to 'path.json'.  
|- 'GUI readme.md'	gui readme file / usage file
|- 'gui_lock_app.py'	gui logic  
|- 'icon-5355895_1280'	main icon for gui app  
|- 'LICENSE'		license file  
|- 'main_lock.py'	Module that work with windows security descriptors inside folder.  
|- 'startwindows.manifest'	manifest file used for granting administrator rights for compiled .exe  
|- 'password.json'	File that hold encrypted password. It will be created after running the program.   
|- 'path.json'		File that hold path to the last locked/unlocked folder  
|- 'readme.md'		This file  
|- 'startwindows.py'	PyQt6 GUI app  

## Dependencies

Dependencies are listed in 'dependencies.txt' file  

## Buy me a coffee

If my tool has helped you or you use it in your business every day, I would appreciate it if you buy me a coffee:  

Paypal : net_hr@outlook.com  
Monero : 49D8Vbe2cpsiWxHhgjfExz2NECvdoaZhoJS33gaiUbPhY2PJZQuQfsbhR7pyGsxaEP4UkPhiWz6kCc9j7YzVs1psTMHxo4G  
Ethereum : 0x33234686d42eb8b2f96f75f061bc01a302515014  
Ethereum Classic : 0x33234686d42eb8b2f96f75f061bc01a302515014  
Avalanche AVAX : 0xEEcc1d4c922b66C174600455290ddfAA9f07c73F  

## Licence

**MIT License**

Copyright (c) [2023] [Emir Hasanica] [emir002@yahoo.com]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.  


