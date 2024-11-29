from common import positions_by_table_size
import random
from poker.hand import Hand

class PreflopScenario:
    def __init__(self, table_size=6):
        self.villain_position: str = None
        self.villain_stack: float = None
        self.villain_cards: str = None

        self.hero_position: str = None
        self.hero_stack: float = None
        self.hero_cards: str = None

        self.table_size: int = table_size

    def generate_seed(self) -> None:
        #get two random positions
        num1, num2 = random.randint(0, self.table_size), random.randint(0, self.table_size)
        while num2 == num1: num2 = random.randint(0, self.table_size)

        #set positions
        self.villain_position = positions_by_table_size[self.table_size][num1]
        self.hero_position = positions_by_table_size[self.table_size][num2]

        #set stacks (equal for now)
        self.hero_stack = 100
        self.villain_stack = 100

        #give random hands
        self.hero_cards = Hand.make_random()
        self.villain_cards = Hand.make_random()

        print(self.hero_cards, self.hero_position)
        print(self.villain_cards, self.villain_position)


    def solve_scenario(self) -> None:
        '''use the hero hand, position and position of villain with range charts to determine the optimal decision.'''
        pass
        


if __name__ == "__main__":
    p = PreflopScenario()
    p.generate_seed()