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
    

