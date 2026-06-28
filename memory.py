import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create full path to memory.json
MEMORY_FILE = os.path.join(BASE_DIR, "memory.json")

def load_memory():
    if os.path.exists(MEMORY_FILE):#If the file exists → load it,If not → return empty memory
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_memory(messages):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)