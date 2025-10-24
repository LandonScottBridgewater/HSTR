import json

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load {path}: {e}")