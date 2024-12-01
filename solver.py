
from dataclasses import dataclass
from Range import Range
import numpy as np
from Cards import Cards
import random

@dataclass(frozen=True)
class Action: #this represents a single action made by a player
    player: str #either "hero" or "villain"
    action_type: str #call, bet, raise, fold, check
    amount: float #some amount of big blinds
    position: str #position at the table


regret_sum = {} #regret for each possible action at a particular state. k = info_set, v = regrets map, where k=decision, v=regret
strategy_sum = {}
card_utils = Cards()




def sample_hand_from_range(range_obj: Range, history: list[Action], player: str, used_cards: list) -> str:
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
    

    sampled_generic_hand = np.random.choice(hands, p=probabilities)
    possible_specific_hands = card_utils.get_specific_hands(sampled_generic_hand, used_cards)
    if not possible_specific_hands:
        raise Exception(f"sample_hand_from_range() Error: CANNOT DRAW HAND FROM DECK!")
    specific_hand = random.choice(possible_specific_hands)
    return sampled_generic_hand, specific_hand



def get_player_contribution(player, history):
    '''gets the amount of money a player has contributed to the pot'''
    total = 0
    for action in history:
        if action.player_type == player:
            total += action.amount
    return action


def terminal_utility(state, history, player):
    last_action = history[-1] #get last action of hand

    #get both players hands for possible showdown
    hero_hand = state.get('hero_specific_hand') 
    villain_hand = state.get('villain_specific_hand')
    
    #if someone folds
    if last_action.action_type == 'fold':
        if last_action.player == player:
            return -1 * get_player_contribution(player, history)
        else:
            return state['current_pot'] - get_player_contribution(player, history)
    else:
        #TODO: compare hands of both players, find which one wins
        return 0





def get_strategy(info_set):
    '''
    Compute the optimal strategy based on the regret values of each possible immediate decision.
    This function is called after the decision tree is already made, and regret is calculated from terminal branches.
    This function simply adds and average that regret to get the best immediate decision.

    @params
    info_set : tuple(player_hand: str, history: list[Action])
        This is essentially a minimal state of the game.
    
    '''
    regrets = regret_sum[info_set] #get regret at this state of the game where k=decision, v=regret
    normalizing_sum = sum([max(r, 0) for r in regrets.values()]) #get cumulative sum of all positive regret values
    strategy = {}

    if normalizing_sum > 0: #if there is positive regret for any of the immediate decisions here
        for action in regrets:
            strategy[action] = max(regrets[action], 0) / normalizing_sum
            #this computes the regret relative to other actions in the set of possible immediate decisions.
    else:
        num_actions = len(regrets) if regrets else 1
        for action in regrets:
            strategy[action] = 1.0 / num_actions

    # update strategy sums for averaging
    for action in strategy:
        strategy_sum[info_set][action] += strategy[action]
    return strategy

def is_terminal_state(history, board, prev_board):
    #if no cards have been shown yet or no bets have been made yet, we definitely haven't reached a terminal state
    if not history or not len(history) or not board: return False
    #if last action was either call or fold and we haven't just turned over a new card, we've reached a terminal state
    if len(board) == len(prev_board) == 5 and history[-1].action_type in ['call','fold']: return True





def get_decision_tree(current_bet: float, current_pot: float, current_stack: float, villain_stack: float) -> dict:
    assert min(current_stack, villain_stack) > 0 #there are no betting decisions to be made if the effective stack size is 0
    '''gets decision tree based on current game. all variables are in terms of big blinds (BB)'''
    #not including third pot for now for combinatorial explosion's sake
    effective_stack_size = min(current_stack, villain_stack)
    half_pot, third_pot = current_pot // 2, current_pot // 3
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
    

deck = card_utils.generate_deck()

example_state = {
    'board': [],
    'villain_range': Range(),
    'hero_range': Range(),
    'hero_generic_hand': None,
    'hero_specific_hand': None,
    'villain_generic_hand': None,
    'villain_specific_hand': None,
    'current_bet': 0,
    'current_pot': 0,
    'hero_stack': 34,
    'villain_stack': 30,
    'hero_position': 'BB',
    'villain_position': 'SB',
    'deck' : deck,
}




def cfr(state: dict, history, probabilities: dict, player: str, reach_probability: float, depth: int = 0, prev_state: dict = None):
    """
    @params
    state : dict
        k=game state attribute, v=value of that attribute. stores the current state;
        current bet, current pot, and both players' stacks.
    history : list[Action]
        a list of Action objects which represent actions by either player
    probabilities: dict
        ...
    """
    opponent = 'villain' if player == 'hero' else 'hero' #set opponent for usage later
    plays = history

    # Check for terminal state
    if is_terminal_state(plays, state['board'], prev_state['board']):
        return terminal_utility(state, history, player)

    # Sample hands for players if not already done
    if player == 'hero':
        if 'hero_specific_hand' not in state or state['hero_specific_hand'] == None:

            #randomly draw a hand from the range
            hero_generic_hand, hero_specific_hand = sample_hand_from_range(
                state['hero_range'], plays, player, state['deck'], state['used_cards']
            )

            #set cards in state
            state['hero_generic_hand'] = hero_generic_hand
            state['hero_specific_hand'] = hero_specific_hand

            #remove randomly drawn cards from deck
            state['deck'].remove(hero_specific_hand[0])
            state['deck'].remove(hero_specific_hand[1])
    else:
        if 'villain_specific_hand' not in state or state['villain_specific_hand'] == None:

            #randomly draw a hand from the range
            villain_generic_hand, villain_specific_hand = sample_hand_from_range(
                state['villain_range'], plays, player, state['deck'], state['used_cards']
            )

            #set cards in state
            state['villain_generic_hand'] = villain_generic_hand
            state['villain_specific_hand'] = villain_specific_hand

            #remove randomly drawn cards from deck
            state['deck'].remove(villain_specific_hand[0])
            state['deck'].remove(villain_specific_hand[1])

    #TODO: add a function to manage the board, keeping in mind whatever action there is. look at is_terminal for inspiration.
    #TODO: create a function to evaluate a hand at showdown, with a return value of like "2 pair" or something idk
    #TODO: evaluate info_set and determine if we should include our board in there.

    # turn the player's hand and the history into mutable tuple types so they can be hashed into regret_sum
    info_set = (state['hero_generic_hand'], plays) if player == 'hero' else (state['villain_generic_hand'], plays)

    # get the strategy for this info_set
    strategy = get_strategy(info_set, state, player, reach_probability)
    action_utilities = {}
    node_utility = 0.0

    # get all possible actions for this state
    actions = get_decision_tree(
        state['current_bet'],
        state['current_pot'],
        state['hero_stack'] if player == 'hero' else state['villain_stack'],
        state['villain_stack'] if player == 'hero' else state['hero_stack']
    )

    # iterate through the possible actions
    for action_dict in actions:
        action_type = action_dict['action']
        amount = action_dict['amount']
        position = state['hero_position'] if player == 'hero' else state['villain_position']
        action = Action(player=player, action_type=action_type, amount=amount, position=position)
        next_state = state.copy()
        next_state = next_state.copy()
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
            action_utility = -cfr(next_state, next_history, new_probabilities, opponent, next_reach_probability, depth+1, state)
            action_utilities[action_type] = action_utility #store utility of every possible immediate decision/action
            node_utility += action_prob * action_utility #add up utility of each action/decision

    #update regrets
    for action_type in strategy.keys():

        #how much better or worse was this particular action relative to all the other immediate actions in this node?
        regret = action_utilities.get(action_type, 0) - node_utility

        #update based on this regret value
        regret_sum[info_set][action_type] += reach_probability * regret

    return node_utility


