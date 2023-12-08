# 002 Folder Lock

## Summary
002 Folder lock is a tool for simply locking folders in the Windows system with a password. Locked folders cannot be accessed from Windows, they cannot be deleted or copied.
002 Folder Lock works by modifying windows security descriptors at the folder level. You can read about them here: [windows security descriptors.](https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptors)
**Note:** Never store important passwords or credit card numbers in a locked folder! 002 Folder Lock prohibits access to the folder from the windows platform only. The files in the locked folder are not encrypted at all. The program is designed for simplicity and speed of use, not for ultimate security. If you want security as much as Windows can provide use this program in combination with Bitlocker or other encription utility.

## Overview
When the user starts the program for the first time, he will be prompted to enter a new password. It is very important that the user remembers the password or writes it down in a safe place because once the password is set it cannot be recovered. After the user sets the password, the main screen will open.
There are four buttons on the main screen. The "Change folder" button is used to select the folder that will be locked. The exact path to the folder is written in the field in front of the button, and it always refers to the current folder. The other buttons are "Unlock folder", Lock folder" and "Exit" which are self-explanatory. Note: When the user selects a folder, the field "Current folder status" automatically detects the status of the folder. If the status is "Unlocked" and is blue, it means that folder is currently unlocked and can be only locked. If the status is "Locked" and is red, it means that folder is currently locked and can be only unlocked. 

At the top on the left is the "Options" menu. It has the following functions: -Change password, -Help (this file), -Buy me a coffee and -About. The -Change password option opens the next window in which the user must enter the old password and confirm the new password twice. After clicking the OK button, the new password will be used to access the program

##Speed
When unlocking or locking a folder, if there are a large number of files or these files take up a lot of space measured in gigabytes, it is normal for the program to become unresponsive until it finishes all encryption/decryption operations. This may take some time and depends on the size of the folder as well as the speed of your SSD/HDD disk and processor. It is recommended that the program is not interrupted until it is finished. Give him some time.

## More help
You can find more help in file README.md in program directory

## Buy me a coffee

If my tool has helped you or you use it in your business every day, I would appreciate it if you buy me a coffee:

Paypal : net_hr@outlook.com
Monero : 49D8Vbe2cpsiWxHhgjfExz2NECvdoaZhoJS33gaiUbPhY2PJZQuQfsbhR7pyGsxaEP4UkPhiWz6kCc9j7YzVs1psTMHxo4G
Ethereum : 0x33234686d42eb8b2f96f75f061bc01a302515014
Ethereum Classic : 0x33234686d42eb8b2f96f75f061bc01a302515014
Avalanche AVAX : 0xEEcc1d4c922b66C174600455290ddfAA9f07c73F  
