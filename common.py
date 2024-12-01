
positions_by_table_size = {
    2: ['BTN', 'BB'],
    3: ['BTN', 'SB', 'BB'],
    4: ['BTN', 'SB', 'BB', 'UTG'],
    5: ['BTN', 'SB', 'BB', 'UTG', 'CO'],
    6: ['BTN', 'SB', 'BB', 'UTG', 'HJ', 'CO'],
    7: ['BTN', 'SB', 'BB', 'UTG', 'MP', 'HJ', 'CO'],
    8: ['BTN', 'SB', 'BB', 'UTG', 'MP', 'MP+1', 'HJ', 'CO'],
    9: ['BTN', 'SB', 'BB', 'UTG', 'UTG+1', 'MP', 'MP+1', 'HJ', 'CO'],
}



hand_rankings = ['AA', 'KK', 'QQ', 'AKs', 'JJ', 'AQs', 'KQs', 'AJs', 'KJs', 
                 'TT', 'AKo', 'ATs', 'QJs', 'KTs', 'QTs', 'JTs', '99', 'AQo', 
                 'A9s', 'KQo', '88', 'K9s', 'T9s', 'A8s', 'Q9s', 'J9s', 'AJo', 
                 'A5s', '77', 'A7s', 'KJo', 'A4s', 'A3s', 'A6s', 'QJo', '66', 
                 'K8s', 'T8s', 'A2s', '98s', 'J8s', 'ATo', 'Q8s', 'K7s', 'KTo', 
                 '55', 'JTo', '87s', 'QTo', '44', '33', '22', 'K6s', '97s', 'K5s',
                   '76s', 'T7s', 'K4s', 'K3s', 'K2s', 'Q7s', '86s', '65s', 'J7s',
                     '54s', 'Q6s', '75s', '96s', 'Q5s', '64s', 'Q4s', 'Q3s', 'T9o',
                       'T6s', 'Q2s', 'A9o', '53s', '85s', 'J6s', 'J9o', 'K9o', 'J5s',
                         'Q9o', '43s', '74s', 'J4s', 'J3s', '95s', 'J2s', '63s', 'A8o',
                           '52s', 'T5s', '84s', 'T4s', 'T3s', '42s', 'T2s', '98o', 'T8o',
                             'A5o', 'A7o', '73s', 'A4o', '32s', '94s', '93s', 'J8o', 
                             'A3o', '62s', '92s', 'K8o', 'A6o', '87o', 'Q8o', '83s', 
                             'A2o', '82s', '97o', '72s', '76o', 'K7o', '65o', 'T7o',
                               'K6o', '86o', '54o', 'K5o', 'J7o', '75o', 'Q7o', 'K4o', 
                               'K3o', '96o', 'K2o', '64o', 'Q6o', '53o', '85o', 'T6o', 
                               'Q5o', '43o', 'Q4o', 'Q3o', '74o', 'Q2o', 'J6o', '63o', 
                               'J5o', '95o', '52o', 'J4o', 'J3o', '42o', 'J2o', '84o', 
                               'T5o', 'T4o', '32o', 'T3o', '73o', 'T2o', '62o', 
                               '94o', '93o', '92o', '83o', '82o', '72o']



if __name__ == "__main__":
    #print(get_decision_tree(0, 400, 50, 80))
    pass
