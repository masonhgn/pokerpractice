import json
import numpy as np
from Cards import Cards

class Range:
    def __init__(self, file_name: str = None):
        if file_name:
            self.load_range_file(file_name)
        else:
            self.load_default_empty_range()

    def load_range_file(self, file_name: str):
        with open(file_name, "r") as f:
            file_dict: dict = json.load(f)
        self.range = file_dict['range']
        self.hero_position = file_dict['hero_position']
        #self.villain_position = file_dict['villain_position']

    def load_default_empty_range(self):
        self.range = {}
        metrics = {
            'trials': 0,
            'reward': 0,
        }
        cards = Cards()
        hands = cards.generate_hands_for_range_chart()
        for hand in hands:
            self.range[hand]['decisions'] = {
                'call': metrics, 
                '3bet': metrics, 
                'check_or_fold': metrics,
            }
            self.range[hand]['alpha'] = {
                'call': 1,
                '3bet': 1, 
                'check_or_fold': 1
            }

    def probabilities(self, hand):
        # get probabilities from Dirichlet parameters
        total = sum(self.alpha.values())
        alphas = self.range[hand]['alpha']
        return {action: alphas[action] / total for action in alphas.keys()}

    def adjust_hand(self, hand: str, action: str, reward: float, eta: float = 0.05):
        """update alpha params based on outcome"""     
        probs = self.probabilities()
        adjustment = eta * np.tanh(reward) * (1 / probs[action])
        self.range[hand]['alpha'][action] += adjustment
        self.range[hand]['alpha'][action] = max(self.range[hand]['alpha'][action], 0.01) #make sure we stay > 0
        self.range[hand]['decisions'][action]['trials'] += 1
        self.range[hand]['decisions'][action]['reward'] += reward

    def save_range_file(self, file_name):
        json_dict = {}
        json_dict['range'] = self.range
        json_dict['hero_position'] = self.hero_position
        with open(file_name, 'w') as f:
            json.dump(json_dict)
