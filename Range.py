import json
import numpy as np
from Cards import Cards


one_third: float = float(1/3)

class Range:
    def __init__(self, file_name: str = None):
        if file_name:
            self.load_range_file(file_name)
        else:
            self.load_default_uniform_range()

    def load_default_uniform_range(self):
        self.range = {}
        cards = Cards()
        hands = cards.generate_hands_for_range_chart()
        for hand in hands:
            self.range[hand] = {
                'raise': one_third,
                'call': one_third,
                'check_or_fold': one_third,
            }
        self.hero_position = None
        self.villain_position = None

    def load_range_file(self, file_name: str):
        with open(file_name, "r") as f:
            file_dict: dict = json.load(f)
        self.range = file_dict['range']
        self.hero_position = file_dict['hero_position']
        self.villain_position = file_dict['villain_position']

    def save_range_file(self, file_name):
        json_dict = {}
        json_dict['range'] = self.range
        json_dict['hero_position'] = self.hero_position
        json_dict['villain_position'] = self.villain_position
        with open(file_name, 'w') as f:
            json.dump(json_dict, f)
