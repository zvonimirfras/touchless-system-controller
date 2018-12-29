"""Loads, serves and saves settings from and to json"""

import json

class Settings():
    """Settings class"""

    def __init__(self, settings_path="settings.json"):
        self.data = {}
        self.load(settings_path)

    def __getattr__(self, name):
        if name not in self.data:
            return None

        return self.data[name]

    def load(self, settings_path="settings.json"):
        """Loads settings from json"""
        with open(settings_path) as settings:
            self.data = json.load(settings)

    def save(self, settings_path="settings.json"):
        """Saves settings to json"""
        with open(settings_path, "w") as settings:
            json.dump(self.data, settings)
