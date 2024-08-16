import json
import os
from utils.utils import get_abs_path

class Config:
    def __init__(self, file_path='/assets/config.json'):
        self.filename = get_abs_path(file_path)
        self.config_data = {}
        self.load()

    def load(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                file_content = file.read()
                self.config_data = json.loads(file_content)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get(self, key):
        keys = key.split('.')
        value = self.config_data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        return value

    def set(self, key, value):
        keys = key.split('.')
        obj = self.config_data
        for k in keys[:-1]:
            if k not in obj:
                obj[k] = {}
            obj = obj[k]
        obj[keys[-1]] = value
        self.config_data = obj
        self.save()

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.config_data, file, indent=4, ensure_ascii=False)


config = Config()