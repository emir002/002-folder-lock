import os
import json

def read_path_file():
    if os.path.exists('path.json'):
        with open('path.json', 'r') as f:
            data = json.load(f)
            return data
    else:
        return {}

def write_path_file(data):
    with open('path.json', 'w') as f:
        json.dump(data, f, indent=4)

def save_load_path():
    data = read_path_file()
    
""""    if 'folder_path' in data:
        print(data['folder_path'])
        
    else:
        print("Please enter folder path:")
        folder_path = input().strip()
        data['folder_path'] = folder_path
        write_path_file(data)
        
        
        
                
        elif choice == '3':
            print("Quitting...")
            break

if __name__ == "__main__":
    save_load_path()
"""
