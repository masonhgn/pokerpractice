
from dataclasses import dataclass
from Range import Range
import numpy as np
from Cards import Cards
import random
import copy

@dataclass(frozen=True)
class Action: #this represents a single action made by a player
    player: str #either "hero" or "villain"
    action_type: str #call, bet, raise, fold, check
    amount: float #some amount of big blinds
    position: str #position at the table




class Solver:
    def __init__(self):
        self.regret_sum = {}
        self.strategy_sum = {}
        self.card_utils = Cards()









    def sample_hand_from_range(self, range_obj: Range, history: list[Action], player: str, used_cards: set) -> str:
        '''
        @params
        range_obj : Range
            The range we are sampling from
        history : list[Action]
            The history of actions taken by all players
        player: str
            Either 'hero' or 'villain'
        '''

        #get last action of player
        last_action = None
        for action in reversed(history):
            if action.player == player:
                last_action = action
                break

        #if the player has not acted, we're just using default range 
        if last_action is None:
            action_type = 'default'
        else: action_type = last_action.action_type


        #get all hands in range
        hands = list(range_obj.range.keys())
        probabilities = []

        #aggregate probabilities the specific action_type we're working with
        for hand in hands:

            #the probability that this action will be done for this hand
            action_prob = range_obj.range[hand].get(action_type, 0)

            #collect all probabilities of this action for sampling purposes
            probabilities.append(action_prob)
        
        #normalize probabilities
        total_prob = sum(probabilities)

        #if there are no hands in this range that match this action type (maybe if it's a super tight range or something)
        if total_prob == 0: probabilities = [1/len(probabilities)] * len(probabilities) #avoid division by 0
        else: probabilities = [p / total_prob for p in probabilities] #calculate relative probabiltiies
        
        possible_specific_hands = None
        while not possible_specific_hands:
            sampled_generic_hand = np.random.choice(hands, p=probabilities)
            possible_specific_hands = self.card_utils.get_specific_hands(sampled_generic_hand, used_cards)
        specific_hand = random.choice(possible_specific_hands)
        used_cards.update(specific_hand)
        return sampled_generic_hand, specific_hand













    def get_player_contribution(self, player, history):
        '''gets the amount of money a player has contributed to the pot'''
        total = 0
        for action in history:
            if action.player == player:
                total += action.amount
        return total












    def terminal_utility(self, state, history, player):
        
        last_action = history[-1] #get last action of hand

        #get both players hands for possible showdown
        hero_hand = state.get('hero_specific_hand') 
        villain_hand = state.get('villain_specific_hand')
        
        #if someone folds
        if last_action.action_type == 'fold':
            if last_action.player == player:
                return -1 * self.get_player_contribution(player, history)
            else:
                return state['current_pot'] - self.get_player_contribution(player, history)
        else:
            #calculate which hand won based on the river
            winner = self.card_utils.evaluate_hands(hero_hand, villain_hand, state['board'])

            if winner == 'hand1': #hero wins hand
                if player == 'hero': return state['current_pot'] - self.get_player_contribution('hero',history)
                else: return -self.get_player_contribution('villain',history)
            elif winner == 'hand2': #villain wins hand
                if player == 'hero': return -self.get_player_contribution('hero',history)
                else: return state['current_pot'] - self.get_player_contribution('villain',history)
            else: #split pot
                return (state['current_pot'] / 2) - self.get_player_contribution(player, history)

















    def get_strategy(self, info_set, action_types):
        '''
        Compute the optimal strategy based on the regret values of each possible immediate decision.
        This function is called after the decision tree is already made, and regret is calculated from terminal branches.
        This function simply adds and average that regret to get the best immediate decision.

        @params
        info_set : tuple(player_hand: str, history: list[Action])
            This is essentially a minimal state of the game.
        
        '''
        if info_set not in self.regret_sum:
            self.regret_sum[info_set] = {action: 0.0 for action in action_types}

        regrets = self.regret_sum[info_set]
        normalizing_sum = sum(max(r, 0) for r in regrets.values())
        strategy = {}

        if normalizing_sum > 0:
            for action in action_types:
                strategy[action] = max(regrets[action], 0) / normalizing_sum
        else:
            num_actions = len(action_types)
            for action in action_types:
                strategy[action] = 1.0 / num_actions

        # Initialize strategy_sum entry if not present
        if info_set not in self.strategy_sum:
            self.strategy_sum[info_set] = {action: 0.0 for action in action_types}

        # Update strategy sums
        for action in action_types:
            self.strategy_sum[info_set][action] += strategy[action]

        return strategy
    
















    def is_terminal_state(self, history, board, prev_board, state):

        #if either player has already gone all in, there is no more action to occur
        if min(state['hero_stack'], state['villain_stack']) == 0: return True
        
        #if no cards have been shown yet or no bets have been made yet, we definitely haven't reached a terminal state
        if not history or not len(history) or not board: return False

        #is_betting_round_complete() doesn't guarantee that we've reached a terminal state, but 
        #if it returns false, we definitely haven't reached a terminal state.
        if not self.is_betting_round_complete(history): return False


        #if someone folded, we're reached a terminal state (ONLY WORKS IN HEADS UP)
        if history[-1].action_type == 'fold': return True

        #since betting rounds are complete, if this board and prev_board are both the river then that means
        #our betting rounds are complete and those bets definitely occurred after the river card.
        #this means that we're reached a terminal state.
        if len(board) == 5 and len(prev_board) == 5: return True

        return False



















    def get_decision_tree(self, current_bet: float, current_pot: float, current_stack: float, villain_stack: float) -> list:
        assert min(current_stack, villain_stack) > 0 #there are no betting decisions to be made if the effective stack size is 0
        '''gets decision tree based on current game. all variables are in terms of big blinds (BB)'''
        #not including third pot for now for combinatorial explosion's sake
        effective_stack_size = min(current_stack, villain_stack)
        half_pot, third_pot = max(current_pot // 2, 1), max(current_pot // 3, 1)
        check_action, fold_action = {'action': 'check', 'amount': 0}, {'action': 'fold', 'amount': 0}
        call_action = {'action': 'call', 'amount': min(current_bet, effective_stack_size)}

        possible_bet_actions = []
        if effective_stack_size >= 3:
            possible_bet_actions.append({'action': 'bet', 'amount': 3})
            # if effective_stack_size >= third_pot:
            #     possible_bet_actions.append({'action': 'bet', 'amount': third_pot})
            if effective_stack_size >= half_pot:
                possible_bet_actions.append({'action': 'bet', 'amount': half_pot})

        possible_raise_actions = []
        if effective_stack_size >= current_bet * 2: #min raise
            possible_raise_actions.append({'action': 'raise', 'amount': current_bet*2})

        #build decision tree
        if (current_bet == 0):
            #either we can check, or do the above scenarios
            possible_actions = [check_action]
            if len(possible_bet_actions): possible_actions += possible_bet_actions
            return possible_actions
        else: #player bets to you
            possible_actions = [call_action, fold_action]
            if len(possible_raise_actions): possible_actions += possible_raise_actions
            return possible_actions
        

    def is_betting_round_complete(self, history):
        #nobody betted anything yet or only one person betted
        if not history or len(history) < 2: return False
        last_action = history[-1]
        second_last_action = history[-2]

        #player folded, hand definitely over
        if last_action.action_type == 'fold':
            return True
        #player called, betting is over for this street
        if last_action.action_type == 'call':
            return True
        #both players checked
        if last_action.action_type == 'check' and second_last_action.action_type == 'check':
            return True

        return False




    def update_board(self, state):
        if state['street'] == 'preflop':
            #deal flop
            board_cards = random.sample(state['deck'], 3)
            for card in board_cards:
                state['deck'].remove(card)
                state['used_cards'].add(card)
            state['board'].extend(board_cards)
            state['street'] = 'flop'
        elif state['street'] == 'flop':
            #deal turn
            board_card = random.choice(state['deck'])
            state['deck'].remove(board_card)
            state['used_cards'].add(board_card)
            state['board'].append(board_card)
            state['street'] = 'turn'
        elif state['street'] == 'turn':
            #deal river
            board_card = random.choice(state['deck'])
            state['deck'].remove(board_card)
            state['used_cards'].add(board_card)
            state['board'].append(board_card)
            state['street'] = 'river'



    def remove_cards_from_deck(self, cards, deck, used_cards):
        for card in cards:
            deck.remove(card)
            used_cards.add(card)




    def initialize_state(
            self,
            villain_range: Range,
            hero_range : Range,
            deck: list,
            used_cards: set = set(),
            board: list = [],
            street: str = 'preflop',
            hero_generic_hand: str = None,
            hero_specific_hand: list = None,
            villain_generic_hand: str = None,
            villain_specific_hand: list = None,
            current_bet: float = 0,
            current_pot: float = 0,
            hero_stack: float = 100,
            villain_stack: float = 100,
            hero_position: str = 'BB',
            villain_position: str = 'SB',
    ) -> dict:
        
        ##make sure the street variable is consistent with the board
        assert (
            street == 'preflop' and not len(board) or
            street == 'flop' and len(board) == 3 or
            street == 'turn' and len(board) == 4 or
            street == 'river' and len(board) == 5
        )

        '''
        there are 4 cases we will have regarding hand args

        1. generic hand but no specific hand
            - we set a specific hand based on the available cards in the deck
            - take the specific hand out of the deck
        2. specific hand but no generic hand
            - take the specific hand out of the deck
        3. generic and specific hand
            - assert that the specific hand is possible with the deck
            - take the specific hand out of the deck
        4. neither
            - do nothing


            CURRENTLY GETTING ERROR:

                        Traceback (most recent call last):
            File "/Users/duck/Documents/projects/python/pokerpractice/solver.py", line 714, in <module>
                preflop_range = solver.build_preflop_range('BB', 'SB')
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            File "/Users/duck/Documents/projects/python/pokerpractice/solver.py", line 685, in build_preflop_range
                state = self.initialize_state(
                        ^^^^^^^^^^^^^^^^^^^^^^
            File "/Users/duck/Documents/projects/python/pokerpractice/solver.py", line 384, in initialize_state
                hero_specific_hand = random.choice(specific_hands)
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/random.py", line 347, in choice
                raise IndexError('Cannot choose from an empty sequence')
            IndexError: Cannot choose from an empty sequence

            TODO: FIX THIS
        '''
        if hero_generic_hand and not hero_specific_hand: #case 1
            specific_hands = self.card_utils.get_specific_hands(hero_generic_hand, used_cards)
            hero_specific_hand = random.choice(specific_hands)
            self.remove_cards_from_deck(hero_specific_hand, deck, used_cards)
        elif hero_specific_hand and not hero_generic_hand: #case 2
             self.remove_cards_from_deck(hero_specific_hand, deck, used_cards)
        elif hero_generic_hand and hero_specific_hand: #case 3
            assert set(hero_specific_hand) <= self.card_utils.get_specific_hands(hero_generic_hand, used_cards)
            self.remove_cards_from_deck(hero_specific_hand, deck, used_cards)


        if villain_generic_hand and not villain_specific_hand: #case 1
            specific_hands = self.card_utils.get_specific_hands(villain_generic_hand, used_cards)
            villain_specific_hand = random.choice(specific_hands)
            self.remove_cards_from_deck(villain_specific_hand, deck, used_cards)
        elif villain_specific_hand and not villain_generic_hand: #case 2
            self.remove_cards_from_deck(villain_specific_hand, deck, used_cards)
        elif villain_generic_hand and villain_specific_hand: #case 3
            assert set(villain_specific_hand) <= self.card_utils.get_specific_hands(villain_generic_hand, used_cards)
            self.remove_cards_from_deck(villain_specific_hand, deck, used_cards)




        return {
            'villain_range': villain_range,
            'hero_range': hero_range,
            'deck': deck,
            'used_cards': used_cards,
            'board': board,
            'street': street,
            'hero_generic_hand': hero_generic_hand,
            'hero_specific_hand': hero_specific_hand,
            'villain_generic_hand': villain_generic_hand,
            'villain_specific_hand': villain_specific_hand,
            'current_bet': current_bet,
            'current_pot': current_pot,
            'hero_stack': hero_stack,
            'villain_stack': villain_stack,
            'hero_position': hero_position,
            'villain_position': villain_position
        }
        








    def cfr(
            self, 
            state: dict, 
            history,
            probabilities: dict, 
            player: str, 
            reach_probability: float, 
            depth: int = 0, 
            prev_state: dict = None
        ):
        """
        @params
        state : dict
            k=game state attribute, v=value of that attribute. stores the current state;
            current bet, current pot, and both players' stacks.
        history : list[Action]
            a list of Action objects which represent actions by either player
        probabilities: dict
            has a k=player (just for two players), v = probabilities of each player
        player : str
            what player is currently making this specific decision (either 'hero' or 'villain')
        reach_probability : float
            the probability of the current player to reach this point in the decision tree
        depth : int
            keeps track of how deep we are in the recursion tree
        prev_state : like the first arg, except the state of the previous function call
            ...
        """
        opponent = 'villain' if player == 'hero' else 'hero' #set opponent for usage later
        plays = history

        if self.is_terminal_state(plays, state['board'], prev_state['board'] if prev_state else [], state):
            #print('REACHED TERMINAL STATE')
            # If the board is not yet at the river, deal remaining cards
            if len(state['board']) < 5:
                while state['street'] != 'river':
                    self.update_board(state)
            return self.terminal_utility(state, history, player)

        #print('MIN STACK: ', min(state['hero_stack'], state['villain_stack']))

        # Sample hands for players if not already done
        if player == 'hero':
            if not state['hero_specific_hand']:

                #randomly draw a hand from the range
                hero_generic_hand, hero_specific_hand = self.sample_hand_from_range(
                    state['hero_range'], plays, player, state['used_cards']
                )

                #set cards in state
                state['hero_generic_hand'] = hero_generic_hand
                state['hero_specific_hand'] = hero_specific_hand

                #remove randomly drawn cards from deck
                state['deck'].remove(hero_specific_hand[0])
                state['deck'].remove(hero_specific_hand[1])
        else:
            if not state['villain_specific_hand']:

                #randomly draw a hand from the range
                villain_generic_hand, villain_specific_hand = self.sample_hand_from_range(
                    state['villain_range'], plays, player, state['used_cards']
                )

                #set cards in state
                state['villain_generic_hand'] = villain_generic_hand
                state['villain_specific_hand'] = villain_specific_hand

                #remove randomly drawn cards from deck
                state['deck'].remove(villain_specific_hand[0])
                state['deck'].remove(villain_specific_hand[1])

        if self.is_betting_round_complete(history):
            #move to next street if we aren't on the river
            assert state['street'] != 'river' #we shouldn't get this far, is_terminal_state should have caught this
            self.update_board(state) #show another card


        # get all possible actions for this state
        actions = self.get_decision_tree(
            state['current_bet'],
            state['current_pot'],
            state['hero_stack'] if player == 'hero' else state['villain_stack'],
            state['villain_stack'] if player == 'hero' else state['hero_stack']
        )

        if not len(actions):
            #at this point, is_terminal_state() returned False but there are no actions to be made.
            #this only seems to be possible if one or more players went all in.
            pass

        #convert to list for get_strategy() function call
        action_types = [action_dict['action'] for action_dict in actions]

        # turn the player's hand and the history into mutable tuple types so they can be hashed into regret_sum
        if player == 'hero': info_set = (state['street'], state['hero_generic_hand'], plays)
        else: info_set = (state['street'], state['villain_generic_hand'], plays)


        # get the strategy for this info_set
        strategy = self.get_strategy(info_set, action_types)
        action_utilities = {}
        node_utility = 0.0


        # iterate through the possible actions
        for action_dict in actions:
            action_type = action_dict['action']
            amount = action_dict['amount']
            position = state['hero_position'] if player == 'hero' else state['villain_position']
            action = Action(player=player, action_type=action_type, amount=amount, position=position)
            next_state = copy.deepcopy(state)
            next_history = history + (action,)

            #depending on the action, set up the next state to create a new branch in the decision tree
            if action_type == 'fold':
                pass  #terminal action, will be caught next function call
            elif action_type == 'call':
                call_amount = action_dict['amount']
                next_state['current_pot'] += call_amount
                next_state[f'{player}_stack'] -= call_amount
                next_state['current_bet'] = 0
            elif action_type in ['bet', 'raise']:
                bet_amount = action_dict['amount']
                next_state['current_pot'] += bet_amount
                next_state[f'{player}_stack'] -= bet_amount
                next_state['current_bet'] = bet_amount
            elif action_type == 'check':
                pass  #no change to the state



            #recursively call CFR
            action_prob = strategy.get(action_type, 0)
            if action_prob > 0: #if we have a nonzero probability of committing this action


                #here we are updating the probability of each player to get to this state.
                #this is calculated by taking the probabilities of all the previous actions up to this one, and
                #multiplying them together. (multiplication rule of probability)
                new_probabilities = probabilities.copy() #shitty way of passing by value
                new_probabilities[player] *= action_prob #updatae the current player's probability of reaching this node

                #since we're switching cfr call to opponent, we use their reach probability next
                next_reach_probability = new_probabilities[opponent]

                #zero sum game, one player's gain is another's loss so we negate the next cfr, which is meant for the opposite player.
                action_utility = -self.cfr(next_state, next_history, new_probabilities, opponent, next_reach_probability, depth+1, state)
                action_utilities[action_type] = action_utility #store utility of every possible immediate decision/action
                node_utility += action_prob * action_utility #add up utility of each action/decision

        #update regrets
        for action_type in strategy.keys():

            #how much better or worse was this particular action relative to all the other immediate actions in this node?
            regret = action_utilities.get(action_type, 0) - node_utility

            #update based on this regret value
            self.regret_sum[info_set][action_type] += reach_probability * regret

        return node_utility
    








    def calculate_exploitability(self, iteration):
        total_positive_regret = 0
        for info_set in self.regret_sum:
            for action in self.regret_sum[info_set]:
                regret = self.regret_sum[info_set][action]
                if regret > 0:
                    total_positive_regret += regret
        exploitability = total_positive_regret / iteration
        return exploitability








    def calculate_average_regret(self):
        total_regret = 0.0
        num_info_sets = len(self.regret_sum)
        for info_set in self.regret_sum:
            regrets = self.regret_sum[info_set]
            avg_regret = sum(abs(regret) for regret in regrets.values()) / len(regrets)
            total_regret += avg_regret
        average_regret = total_regret / num_info_sets if num_info_sets > 0 else 0
        return average_regret










    def extract_preflop_strategy(self, preflop_strategy):
        #get all infosets that are preflop
        for info_set in self.strategy_sum:
            street = info_set[0]
            if street == 'preflop':
                strategy = self.strategy_sum[info_set] #decisions with their probabilities
                total = sum(strategy.values())
                normalized_strategy = {action: prob / total for action, prob in strategy.items()}
                hand = info_set[1]
                for action in normalized_strategy:
                    if action in ['check','fold']: real_action = 'check_or_fold'
                    preflop_strategy[hand][real_action] += normalized_strategy[action]
        #normalize strats per hand
        for hand in preflop_strategy.keys():
            total = sum(preflop_strategy[hand].values())
            preflop_strategy[hand] = {action: prob / total for action, prob in preflop_strategy[hand].items()}
        return preflop_strategy












    def build_preflop_range(self, hero_pos, villain_pos, max_iterations=100) -> Range:

        range = Range()
        range.load_default_uniform_range()
        range.hero_position = hero_pos
        range.villain_position = villain_pos

        check_interval = 1

        iter = 0
        exploitability = None
        while iter < max_iterations:
            iter += 1

            probabilities = {'hero': 1, 'villain': 1}
            
            state = self.initialize_state(
                villain_range=range,
                hero_range=range,
                deck=self.card_utils.generate_deck(),
                hero_generic_hand='AA',
                hero_position=hero_pos,
                villain_position=villain_pos
            )

            if iter % 2 == 0:
                self.cfr(state, (), probabilities, 'hero', 1.0)
            else:
                self.cfr(state, (), probabilities, 'villain', 1.0)


            if iter % check_interval == 0:
                avg_regret = self.calculate_average_regret()
                print(f"Iteration [{iter}] average regret: {avg_regret}")

            preflop_range = self.extract_preflop_strategy(range.range)
            temp_range = Range()
            temp_range.range = preflop_range
            temp_range.save_range_file('temp_range.json')
        return preflop_range


if __name__ == "__main__":
    solver = Solver()

    preflop_range = solver.build_preflop_range('BB', 'SB')
    print("Preflop Range:")
    for hand, strategy in preflop_range.items():
        print(f"{hand}: {strategy}")
