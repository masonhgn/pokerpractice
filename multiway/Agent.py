
from multiway.RangeManager import RangeManager
import random

class Agent:
    def __init__(self, starting_stack):
        self.stack = starting_stack
        self.table_position = None
        self.action_history = []
        self.ranges = RangeManager()
        self.current_hand = None
        self.rebuys = 0


    def act(self, prev_actions: list, current_hand: str, board: str):
        #make a decision based on the current action, cards and ranges

        #decipher prev_actions to get current bet 
        current_bet = 0
        for action in prev_actions:
            if action['action_type'] in ['raise', 'call']:
                current_bet = max(current_bet, action['amount'])

        #set variables
        decision = random.uniform(0, 1)
        current_range = self.ranges.get_range(self.table_position)
        probabilities = current_range.probabilities()

        cumulative = 0
        chosen_action = None
        for action, prob in probabilities.items():
            cumulative += prob
            if decision <= cumulative:
                chosen_action = action
                break
        
        if chosen_action == 'call':
            stake = min(self.stack, current_bet)
            action_type = 'call'
        elif chosen_action == '3bet':
            stake = min(current_bet * 2, self.stack) if current_bet > 0 else 3  # 3BB if current bet is nothing
            action_type = 'raise'
        elif chosen_action == 'check_or_fold':
            stake = 0
            action_type = 'check' if current_bet == 0 else 'fold'
            
        self.stack -= stake
        return {'action_type': action_type, 'amount': stake}





        