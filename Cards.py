



class Cards:
	def __init__(self):

		#initialize deck
		self.deck = []
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
