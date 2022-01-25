# -----------------------------------------------------------------------------
# Name:		Minesweeper
#
# Author:	 Ian Cramer
# -----------------------------------------------------------------------------



'''
A game of Minesweeper
'''

import tkinter
import sys

from minesweeper import Minesweeper
		


def main():

	# Instantiate a root window
	root = tkinter.Tk()

	# Instantiate a Game object
	gen_game = Minesweeper(root)

	# Enter the main event loop
	root.mainloop()



if __name__ == '__main__':
	main()