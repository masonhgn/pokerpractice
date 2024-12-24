from Cards import Cards
import json

if __name__ == "__main__":
    cards = Cards()
    hands = cards.generate_hands_for_range_chart()
    
    range = {}

    positions = ['BTN','SB','BB','UTG','HJ','CO']



    #range['hero_position'] = None
    #range['villain_position'] = None 
    range['range'] = {}

    metrics = {
        'trials': 0,
        'reward': 0,
    }

    for hand in hands:
        range['range'][hand]['decisions'] = {
            'call': metrics, 
            '3bet': metrics, 
            'check_or_fold': metrics,
        }
        range['range'][hand]['alpha'] = {
            'call': 1,
            '3bet': 1, 
            'check_or_fold': 1
        }

    with open('range1.json', 'w') as f:
        json.dump(range, f)

    