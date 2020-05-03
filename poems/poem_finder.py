import json
from random import choice
from typing import Optional


class PoemFinder():
    def __init__(self, poems_path: str) -> Optional[str]:
        with open(poems_path, 'r') as f:
            self.poems_by_type = json.loads(f.read())

    def get_poem(self, weather_type):
        if weather_type in self.poems_by_type:
            return choice(self.poems_by_type[weather_type])
        else:
            return None
