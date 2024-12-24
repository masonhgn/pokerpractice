from itertools import combinations, product
from treys import Card, Evaluator


class Cards:
	def __init__(self):

		#initialize deck
		self.deck = []
		self.evaluator = Evaluator()
		for suit in "cdhs":
			for rank in "A23456789TJQK":
				self.deck.append(rank+suit)
	
	def generate_hands_for_range_chart(self) -> list:
		"""Generate all 169 poker starting hands in the order of a standard range chart."""
		hands = []
		ranks = "AKQJT98765432"
		for rank1 in ranks:
			for rank2 in ranks:
				if rank1 == rank2:
					hands.append(f"{rank1}{rank2}")
				elif ranks.index(rank1) < ranks.index(rank2):
					hands.append(f"{rank1}{rank2}s")
				else:
					hands.append(f"{rank2}{rank1}o")
		return hands
	
	def pretty_print_range_chart(self, hands) -> None:
		for i in range(1, len(hands)+1):
			print(hands[i-1], end= '    ')
			if i % 13 == 0 and i >= 13: print('\n\n')




	def convert_to_hand_type(self, hand: str) -> str:
		'''converts something like Ac6d into A6o'''
		rank1, suit1 = hand[0], hand[1]
		rank2, suit2 = hand[2], hand[3]
		if suit1 == suit2: return f"{rank1}{rank2}s" if rank1 >= rank2 else f"{rank2}{rank1}s"
		else: return f"{rank1}{rank2}o" if rank1 >= rank2 else f"{rank2}{rank1}o"


	def generate_deck(self):
		suits = ['h', 'd', 'c', 's']
		ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
		deck = [rank + suit for rank in ranks for suit in suits]
		return deck
	

	def get_specific_hands(self, generic_hand, used_cards):
		suits = ['h', 'd', 'c', 's']
		ranks = {'A': 'A', 'K': 'K', 'Q': 'Q', 'J': 'J', 'T': 'T',
				'9': '9', '8': '8', '7': '7', '6': '6', '5': '5',
				'4': '4', '3': '3', '2': '2'}
		generic_rank1 = generic_hand[0]
		generic_rank2 = generic_hand[1]
		suited = 's' in generic_hand
		offsuit = 'o' in generic_hand
		pairs = generic_rank1 == generic_rank2 and 'o' not in generic_hand and 's' not in generic_hand

		possible_hands = []

		if pairs:
			rank = generic_rank1
			available_suits = [s for s in suits]
			for suit1 in suits:
				for suit2 in suits:
					if suit2 != suit1:
						card1 = rank + suit1
						card2 = rank + suit2
						if card1 not in used_cards and card2 not in used_cards:
							possible_hands.append((card1, card2))
		else:
			rank1 = generic_rank1
			rank2 = generic_rank2
			for suit1 in suits:
				for suit2 in suits:
					if suited and suit1 != suit2:
						continue
					if offsuit and suit1 == suit2:
						continue
					card1 = rank1 + suit1
					card2 = rank2 + suit2
					if card1 not in used_cards and card2 not in used_cards and card1 != card2:
						possible_hands.append((card1, card2))

		return possible_hands
	

	def evaluate_hands(self, hand1: str, hand2: str, board: list[str]) -> str:

		hand1_cards = [Card.new(hand1[0]), Card.new(hand1[1])]
		hand2_cards = [Card.new(hand2[0]), Card.new(hand2[1])]
		board_cards = [Card.new(card) for card in board]

		hand1_score = self.evaluator.evaluate(board_cards, hand1_cards)
		hand2_score = self.evaluator.evaluate(board_cards, hand2_cards)

		if hand1_score < hand2_score: return "hand1"
		elif hand1_score > hand2_score: return "hand2"
		return "split"



# if __name__ == "__main__":
# 	c = Cards()
# 	hands = c.get_specific_hands('A6o',['Ad','6h'])
# 	print(hands)