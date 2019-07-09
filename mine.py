from random import sample

EDGE = 1	# length of the edge of the board
MINES = 0 	# number of mines
CHEAT = 'cheat'
BAD_INPUT = 'please enter space-separated coordinates:'
BLANK_LINES = 30
WIN = 'win'
LOSE = 'ouch you lost\nhere\'s the final board:'
TRY_AGAIN = 'try again i guess'


'''
currently only one Game per program
keeps track of the board and how many spaces left
'''
class Game:
	
	def __init__(self):
		self.board = [[None for x in range(EDGE)] for y in range(EDGE)]
		self.remaining = EDGE * EDGE - MINES	# if this is 0, win
	
	def set_board(self):
		for i in range(0, EDGE):
			for j in range(0, EDGE):
				self.board[i][j] = Node()
		mines = sample(range(0, EDGE * EDGE), MINES)
		for m in mines:
			row = m / EDGE
			col = m % EDGE
			self.board[row][col].mine = True
			self.tell_neighbors(row, col)
	
	# given the coordinates of a mine
	# increments neighbor counts of surrounding nodes
	# checked in this order:
		'''
		2 1 3
		4 x 5
		7 6 8
		'''
	def tell_neighbors(self, row, col):
		has_up = row > 0
		has_down = row < EDGE - 1
		has_left = col > 0
		has_right = col < EDGE - 1
		up = row - 1
		down = row + 1
		left = col - 1
		right = col + 1
		# tell row above
		if has_up:
			self.board[up][col].add()
			if has_left:
				self.board[up][left].add()
			if has_right:
				self.board[up][right].add()
		# tell side neighbors
		if has_left:
			self.board[row][left].add()
		if has_right:
			self.board[row][right].add()
		# tell row below
		if has_down:
			self.board[down][col].add()
			if has_left:
				self.board[down][left].add()
			if has_right:
				self.board[down][right].add()
	
	# checks coordinates to see if there's a mine	
	def is_mine(self, row, col):
		return self.board[row][col].mine
	
	# sets a node to display
	def flip(self, row, col):
		n = self.board[row][col]
		if n.display == True:
			return
		n.display = True
		self.remaining -= 1
		
	# called each turn to show progress
	# you can set cheat to True to show everything
	# that's for admin debugging use only!!
	def show(self, cheat=False):
		print ''
		for row in self.board:
			line = '\t'
			for n in row:
				line += n.get_display_value(cheat) + ' '
			print line


'''
each space on the board is a Node instance
'''
class Node:

	def __init__(self):
		self.mine = False		# boolean that says if it's a mine
		self.neighbors = 0		# mine neighbors
		self.display = False	# if you show the value
	
	def add(self):
		self.neighbors += 1
	
	def get_display_value(self, cheat):
		if not self.display and not cheat:
			return '?'
		elif self.mine:
			return 'x'
		elif self.neighbors == 0:
			return ' '
		else:
			return str(self.neighbors)


'''
called if you guess a mine
'''
def lose(game):
	print ''
	print LOSE
	game.show(cheat=True)
	print TRY_AGAIN
	exit(0)


'''
called if you guess all the safe spaces
'''
def win():
	for i in range(BLANK_LINES):
		print ''
	with open(WIN, 'r') as f:
		print f.read()
	exit(0)


def main():
	g = Game()
	g.set_board()
	g.show()
	while(True):
		input = raw_input()
		if input == CHEAT:
			g.show(cheat=True)
			continue
		row, col = [0, 0]
		try:
			row, col = input.split()	
			row = int(row)
			col = int(col)
			if row < 0 or col < 0 or row >= EDGE or col >= EDGE:
				raise ValueError
		except(ValueError):
			print BAD_INPUT
			continue	
		g.flip(row, col)
		if g.is_mine(row, col):
			lose(g)
		g.show()
		if g.remaining == 0:
			win()


main()
		