from solver import sample_hand_from_range, Action
from Range import Range
from common import hand_rankings







if __name__ == "__main__":
    # test_range = Range()
    # test_range.load_default_uniform_range()

    # for i, hand in enumerate(hand_rankings):
    #     hand_strength = (169 - i) / 169
    #     test_range.range[hand]['raise'] = hand_strength
    #     if hand_strength >= 0.7:
    #         test_range.range[hand]['call'] = (1-hand_strength) / 2
    #         test_range.range[hand]['check_or_fold'] = (1 - hand_strength - test_range.range[hand]['call'])
    #     elif hand_strength >= 0.4:
    #         test_range.range[hand]['call'] = (1-hand_strength) / 3
    #         test_range.range[hand]['check_or_fold'] = (1 - hand_strength - test_range.range[hand]['call'])
    #     else:
    #         test_range.range[hand]['call'] = (1-hand_strength) / 4
    #         test_range.range[hand]['check_or_fold'] = (1 - hand_strength - test_range.range[hand]['call'])

    # for hand in ['AA','KK','QQ','JJ','TT','AKs','AQs']:
    #     test_range.range[hand] = {
    #         'raise': 0.99,
    #         'call': 0.01,
    #         'check_or_fold': 0
    #     }
    
    # for hand in hand_rankings:
    #     if hand in ['AA','KK','QQ','JJ','TT','AKs','AQs']: continue
    #     test_range.range[hand] = {
    #         'raise': 0.01,
    #         'call': 0.01,
    #         'check_or_fold': 0.98
    #     }


    # test_range.save_range_file('first_range.json')




    test_range = Range('first_range.json')

    history = [
        Action('villain','bet',5,'SB'),
        Action('hero','check_or_fold',10,'BB'),
    ]

    generic, specific = sample_hand_from_range(test_range,history,'hero', [])
    print(generic, specific)




    


    