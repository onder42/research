import os
import json

class FileHandler:
    """
    Blueprint responsible strictly for low-level file system
    interactions like writing and reading serialized data.
    """
    def save_json(self, data, file_path):
        """Serializes and writes a Python dictionary to a JSON file."""
        if not data:
            return

        # Automatically extract and create the base folder structure if missing
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def open_json(self, file_path):
        """Reads, parses, and returns a structured JSON file if it exists."""
        if not os.path.exists(file_path):
            print(f"[FileHandler Error] No file found at: {file_path}")
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

