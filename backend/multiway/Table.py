from multiway.Agent import Agent
from poker import Card
import random
from Cards import Cards
import random
import common

class Table:
    def __init__(self):
        self.seats: list = []
        self.deck: list = list(Card)
        self.shuffle_cards()
        self.cards_utils = Cards()
        self.button_position: int = 0
        self.current_pot: float = 0
        self.small_blind: float = 1.00
        self.big_blind: float = 2.00
        self.normal_buyin: float = 1000

    def shuffle_cards(self) -> None:
        random.shuffle(self.deck)

    def add_player(self, stack_size: float) -> None:
        self.seats.append(
            Agent(stack_size) #new player
        )

    def place_button(self, position = None) -> None:
        num_players = len(self.seats)
        assert num_players >= 2 and 0 <= position < num_players

        positions = common.positions_by_table_size[num_players]

        if not position:
            self.button_position = random.randint(0, num_players - 1)
        else: self.button_position = position
        rotated_positions = positions[-self.button_position:] + positions[:-self.button_position]
        for i, agent in enumerate(self.seats):
            agent.table_position = rotated_positions[i]


    def increment_button(self) -> None:
        num_players = len(self.seats)
        assert num_players >= 2
        # increment the button position in a circular manner
        new_button_position = (self.button_position + 1) % num_players

        # reassign positions based on the new button position
        self.place_button(new_button_position)

    def deal_cards(self):

        #make sure all players have no cards
        for agent in self.seats:
            agent.current_hand = ''
        self.shuffle_cards()

        for _ in range(2):
            for agent in self.seats:
                agent.current_hand += str(self.deck.pop())
        
        for agent in self.seats:
            agent.current_hand = self.cards_utils.convert_to_hand_type(agent.current_hand)


    def validate_table(self):
        #make sure all players have stacks >= 1 BB, or else make them rebuy or leave
        for agent in self.seats:
            if agent.stack_size < self.big_blind:
                agent.rebuys += 1
                agent.stack_size = self.normal_buyin

        assert len(self.seats) >= 2


    def play_hand(self):
        #take out blinds from SB and BB positions
        #deal cards to all agents
        #let each agent act preflop, continuing until there is no player who has any action left to decide on
        #if all but one player has folded, end hand and transfer pot to winning player
        #draw cards for flop
        #let each agent act once more
        #if all but one player has folded, end hand and transfer pot to winning player
        #draw turn
        #let each agent act once more
        #if all but one player has folded, end hand and transfer pot to winning player
        #draw river
        #let each agent act once more
        #end hand and transfer pot to winning player
        #remove hands from players (agent.current_hand = None)
        #validate table ()
        #increment button
        pass