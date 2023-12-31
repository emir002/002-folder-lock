# 002 Folder Lock version 0.2

## Summary
002 Folder lock is a tool for simply locking folders in the Windows system with a password. Locked folders cannot be accessed from Windows, they cannot be deleted or copied. You can download the compiled version of the tool ready for installation [HERE](https://e.pcloud.link/publink/show?code=tsJy6alK).
002 Folder Lock works by modifying windows security descriptors at the folder level. You can read about them here: [windows security descriptors.](https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptors)
**Note:** Never store important passwords or credit card numbers in a locked folder! 002 Folder Lock prohibits access to the folder from the windows platform only. The files in the locked folder are encrypted using using the Fernet symmetric encryption provided by the cryptography library in Python. While Fernet provides strong encryption, the security of the encrypted data also heavily depends on the security of the key. If the key is compromised, the encryption can be easily broken. The program is designed for simplicity and speed of use, not for ultimate security. If you want security as much as Windows can provide save your key to USB drive or another location physically separated from the computer.

## Overview
When the user starts the program for the first time, he will be prompted to enter a new password. It is very important that the user remembers the password or writes it down in a safe place because once the password is set it cannot be recovered. After the user sets the password, the main screen will open.
There are four buttons on the main screen. The "Change folder" button is used to select the folder that will be locked. The exact path to the folder is written in the field in front of the button, and it always refers to the current folder. The other buttons are "Unlock folder", Lock folder" and "Exit" which are self-explanatory. Note: When the user selects a folder, the field "Current folder status" automatically detects the status of the folder. If the status is "Unlocked" and is blue, it means that folder is currently unlocked and can be only locked. If the status is "Locked" and is red, it means that folder is currently locked and can be only unlocked. 

At the top on the left is the "Options" menu. It has the following functions: -Change password, -Help (this file), -Buy me a coffee and -About. The -Change password option opens the next window in which the user must enter the old password and confirm the new password twice. After clicking the OK button, the new password will be used to access the program

## False positive  
Some antivirus software (such as Avira - tested) falsely report the program after installation as positive for Trojans / ransomware due to encryption modules and block the program from starting. If this happens restore program from antivirus quarantine, add it to the whitelist of the antivirus program and continue using it normally. For your own safety, you can upload the program to one of the online programs for checking the presence of viruses, such as: https://www.eset.com/int/home/online-scanner/ or https://opentip.kaspersky.com

The program is signed with a self-sign certificate that is available in the download folder. To avoid a warning from the antivirus software, it is recommended that you first download the certificate and install it (password is 0000) and only then install the program, so that the antivirus software would be sure that the program has not been changed from the moment of signing to the moment of installation on the computer.

##Speed  
When unlocking or locking a folder, if there are a large number of files or these files take up a lot of space measured in gigabytes, it is normal for the program to become unresponsive until it finishes all encryption/decryption operations. This may take some time and depends on the size of the folder as well as the speed of your SSD/HDD disk and processor. It is recommended that the program is not interrupted until it is finished. Give it some time.

## Increasing security
The default locations for the files are: \AppData\Roaming\002 Folder Lock\attempts - for the number of password attempts and \AppData\Roaming\002 Folder Lock\key.key for the encryption key. The second folder where the password for the folder is located is AppData\Roaming\Vlc1\pas1.json where the encrypted password is located. Moving the Vlc1 folder to the USB stick will permanently lock the program until the original folder is returned to its original location. Moving the Vlc1 and 002 Folder Lock folders to the USB stick will reset the program to its original settings and the program will ask the user to reset the password. All locked folders will be unlocked, however, all files locked with the old password will not be readable, because the program sets a new random encryption key at each initialization. By returning the original Vlc1 and 002 Folder Lock folders to their original locations, the user will be able to unlock and properly access the originally locked folders and files.

Conclusion: for maximum possible security, cut the Vlc1 folder from the \AppData\Roaming\ folder and paste it on the USB stick. To unlock the program again, return the Vlc1 folder to its original location.

## More help
You can find more help in file README.md in program directory in GitHub and app folder:
https://github.com/emir002/002-folder-lock

## Buy me a coffee

If my tool has helped you or you use it in your business every day, I would appreciate it if you buy me a coffee:

Paypal : net_hr@outlook.com
Monero : 49D8Vbe2cpsiWxHhgjfExz2NECvdoaZhoJS33gaiUbPhY2PJZQuQfsbhR7pyGsxaEP4UkPhiWz6kCc9j7YzVs1psTMHxo4G
Ethereum : 0x33234686d42eb8b2f96f75f061bc01a302515014
Ethereum Classic : 0x33234686d42eb8b2f96f75f061bc01a302515014
Avalanche AVAX : 0xEEcc1d4c922b66C174600455290ddfAA9f07c73F  

©Emir Hasanica 2023 emir002@yahoo.com