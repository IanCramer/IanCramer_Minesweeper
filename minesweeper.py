# -----------------------------------------------------------------------------
# Name:		Minesweeper
#
# Author:	 Ian Cramer
# -----------------------------------------------------------------------------



import tkinter
import sys
import random
import datetime



class Minesweeper(object):
	'''
	Tic Tac Toe Game Class. Inherits from object.
	'''
	# Add your class variables if needed here - square size, etc...)
	tile_size = 20
	base_color = 'grey50'
	flag_color = 'indian red'
	colors = ['grey80', 'light blue', 'light green', 'yellow','dodger blue', 'violet red', 'royal blue', 'purple', 'grey65']


	def __init__(self, root, height=10, width=10, num_mines=0):
		'''
		Constructor takes the tkinter root structure. Creates and starts the game.
		'''
		root.title('Minesweeper')
		self.root = root
		self.height = height
		self.width = width
		if num_mines <= 0:
			self.num_mines = (height*width)/10
			if self.num_mines <= 0:
				self.num_mines = 1
		else:
			self.num_mines = num_mines

		# Create Game Data
		self.make_status()
		self.make_mines()
		self.make_neighbor_mines()

		# Create GUI Widgets
		self.make_restart()
		self.make_entries()
		self.draw_board()

		# Create any additional instance variable you need for the game
		self.game_over = False

		# Start the clock
		self.start = datetime.datetime.now()
################################################

	# Game Data

	def make_status(self):
		self.status = []
		for i in range(self.height):
			self.status.append(['None' for j in range(self.width)])

	def make_mines(self):
		self.mines = []
		for i in range(self.height):
			self.mines.append([False for j in range(self.width)])

		mines_gend = 0
		while mines_gend < self.num_mines:
			i = random.randint(0,self.height-1)
			j = random.randint(0,self.width-1)
			if not self.mines[i][j]:
				self.mines[i][j] = True
				mines_gend += 1

	def make_neighbor_mines(self):
		self.neighbor_mines = []
		for i in range(self.height):
			self.neighbor_mines.append([])
			for j in range(self.width):
				self.neighbor_mines[i].append(self.count_neighbor_mines(i,j))

	def count_neighbor_mines(self,x,y):
		num_mines = 0
		for i in range(x-1,x+2):
			if i < 0 or i >= self.height:
				continue
			for j in range(y-1,y+2):
				if j < 0 or j >= self.width:
					continue
				if i == x and j == y:
					continue
				if self.mines[i][j]:
					num_mines+=1
		return num_mines

################################################

	# GUI

	def make_restart(self):
		# Create the restart button widget
		restart_btn = tkinter.Button(self.root, text='Restart', width=20, command=self.restart)
		restart_btn.grid()

	def restart(self):
		"""
		Handles game restart and reconstruction.
		"""
		self.game_over = False
		self.win_lose_label.destroy()
		self.canvas.destroy()

		# Set Size of New Game
		try:
			w = int(self.width_entry.get())
			self.width = w
		except:
			pass
		try:
			h = int(self.height_entry.get())
			self.height = h
		except:
			pass
		try:
			m = int(self.mines_entry.get())
			self.num_mines = m
		except:
			self.num_mines = int((self.width*self.height)/10)
			if not self.num_mines:
				self.num_mines = 1

		self.make_status()
		self.make_mines()
		self.make_neighbor_mines()
		self.draw_board()
		# Restart tbe clock
		self.start = datetime.datetime.now()

	def make_entries(self):
		entry_frame = tkinter.Frame(self.root)
		entry_frame.grid()

		width_label = tkinter.Label(entry_frame, text=' Width: ')
		width_label.pack(side='left')
		self.width_entry = tkinter.Entry(entry_frame, width=4)
		self.width_entry.pack(side='left')

		height_label = tkinter.Label(entry_frame, text='  Height: ')
		height_label.pack(side='left')
		self.height_entry = tkinter.Entry(entry_frame, width=4)
		self.height_entry.pack(side='left')

		mines_label = tkinter.Label(entry_frame, text='  Mines: ')
		mines_label.pack(side='left')
		self.mines_entry = tkinter.Entry(entry_frame, width=4)
		self.mines_entry.pack(side='left')

		pad_label = tkinter.Label(entry_frame,text=' ')
		pad_label.pack(side='left')


	def draw_board(self):
		"""
		Draw a fresh Minesweeper board
		"""
		self.canvas = tkinter.Canvas(self.root, width=self.tile_size * self.width, height=self.tile_size * self.height)
		self.canvas.grid()
		self.canvas.bind('<Button-1>', self.play_explore)
		self.canvas.bind('<Button-3>', self.play_flag)

		self.board = []
		for row in range(self.height):
			for column in range(self.width):
				id = self.canvas.create_rectangle(self.tile_size * column, self.tile_size * row, self.tile_size * (column + 1), self.tile_size * (row + 1), fill=self.base_color)
				self.board.append(id)

		self.win_lose_label = tkinter.Label(self.root, text='', width=20)
		self.win_lose_label.grid()

	def id(self,x,y):
		# Returns the id token for the board square at the x^th column and y^th
		return (y*self.width)+x+1

	def play_explore(self, event):
		"""
		Facilitates playing the game. Takes an event and changes the gui accordingly.
		"""
		items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
		square_id = items[0]
		x = (square_id-1)%self.width
		y = int((square_id-1)/self.width)

		if self.game_over:
			return

		if self.explore(x,y):
			self.bomb()
		else:
			self.check_win()

	def explore(self, x, y):
		# Valid Location?
		if x < 0 or y < 0 or x >= self.width or y >= self.height:
			return False

		# Flagged Location
		if self.status[y][x] == 'Flagged':
			return False

		# Found a Bomb
		if self.mines[y][x]:
			return True

		# Explorable Location?
		if self.status[y][x] == 'None':
			self.status[y][x] = 'Explored'
			n = self.neighbor_mines[y][x]

			tile = self.id(x,y)
			self.canvas.itemconfig(self.id(x,y), fill=self.colors[n])

			w = x*self.tile_size+(self.tile_size/2)
			z = y*self.tile_size+(self.tile_size/2)
			if n:
				self.canvas.create_text(w, z, text=f'{n}')
			else:
				self.canvas.create_text(w, z, text=' ')
			
		else:
			return False

		# If no neighboring bombs, recursively explore neighbors
		if self.neighbor_mines[y][x] == 0:
			neighbors = [(x-1,y-1), (x-1, y),
					 (x-1, y+1), (x,y-1),
					 (x,y+1), (x+1,y-1),
					 (x+1,y), (x+1,y+1)]
			for n in neighbors:
				self.explore(n[0], n[1])

		# No Bombs
		return False

	def play_flag(self, event):
		items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
		square_id = items[0]
		x = (square_id-1)%self.width
		y = int((square_id-1)/self.width)

		if self.game_over:
			return False

		# Valid Location?
		if x < 0 or y < 0 or x >= self.width or y >= self.height:
			return False

		# Flag Location?
		if self.status[y][x] == 'None':
			self.status[y][x] = 'Flagged'

			tile = self.id(x,y)
			self.canvas.itemconfig(self.id(x,y), fill=self.flag_color)

			w = x*self.tile_size+(self.tile_size/2)
			z = y*self.tile_size+(self.tile_size/2)
			self.canvas.create_text(w, z, text='F')

			return True

		# Unflag Location?
		if self.status[y][x] == 'Flagged':
			self.status[y][x] = 'None'

			tile = self.id(x,y)
			self.canvas.itemconfig(self.id(x,y), fill=self.base_color)

			try:
				self.canvas.itemconfig(items[-1], text='')
				self.canvas.delete(items[-1])
			except:
				k = self.tile_size/3
				items = self.canvas.find_overlapping(event.x-k, event.y-k, event.x+k, event.y+k)
				try:
					self.canvas.itemconfig(items[-1], text='')
					self.canvas.delete(items[-1])
				except:
					# Unflagging Did Not Work
					self.status[y][x] = 'Flagged'
					self.canvas.itemconfig(self.id(x,y), fill=self.flag_color)
					return False

			return True


	def bomb(self):
		# Player Loses
		self.win_lose_label.config(text='You lost!   :(')
		self.game_over = True
		# Show Bombs
		for i in range(self.height):
			for j in range(self.width):
				if self.mines[i][j]:
					self.canvas.itemconfig(self.id(j,i), fill='Red')

					w = j*self.tile_size+(self.tile_size/2)
					z = i*self.tile_size+(self.tile_size/2)
					self.canvas.create_text(w, z, text='*')

	def check_win(self):
		"""
		Checks the state of the game and determines if/who the winner is.
		"""
		if self.game_over:
			return

		num_cells = self.height*self.width
		num_explored = 0
		for i in range(self.height):
			for j in range(self.width):
				if self.status[i][j] == 'Explored':
					num_explored += 1

		if num_cells-num_explored == self.num_mines:
			self.game_over = True
			self.end = datetime.datetime.now()
			self.win_lose_label.config(text=f'You Won!   {self.end-self.start}')