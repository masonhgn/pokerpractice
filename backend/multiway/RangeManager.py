from Range import Range
import common

class RangeManager:
    def __init__(self):
        self.ranges = {}

    def generate_default_ranges(self, table_size: int):
        assert 2 <= table_size <= 9
        positions = common.positions_by_table_size[table_size]
        for pos in positions:
            self.ranges[pos] = Range()

    def get_range(self, position):
        return self.ranges[position]
    
    def adjust_range(self, position: str, hand: str, action: list, reward: float, eta: float =0.05):
        self.ranges[position].adjust_hand(hand=hand, action=action,reward=reward,eta=eta)

    