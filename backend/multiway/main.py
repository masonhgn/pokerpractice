from multiway.Table import Table

if __name__ == "__main__":
	table = Table()
	for _ in range(6):
		table.add_player(10000)
	table.deal_cards()
	