#!/usr/bin/env python
#coding:utf-8

from Grid import Grid
from ComputerAI import ComputerAI
from PlayerAI import PlayerAI
from Displayer import Displayer
from random import randint
import time

from pprint import pprint
import gc

defaultInitialTiles = 2
defaultPossibility = 0.9
(PLAYER_TURN, COMPUTER_TURN) = (0, 1)
actionDic = {0:"UP", 1:'DOWN', 2:'LEFT', 3:'RIGHT'}
# time limit for guess time of each step
timeLimit = 1

class GameManager:
	def __init__(self, size = 4):
		# init some variables
		self.grid = Grid(size)
		self.possibleNewTileValue = [2, 4]
		self.possibility = defaultPossibility
		self.initTiles = defaultInitialTiles
		self.computerAI = None
		self.playerAI = None
		self.displayer = None
		self.over = False

	def setComputerAI(self, compAI):
		self.computerAI = compAI

	def setPlayerAI(self, playerAI):
		self.playerAI = playerAI

	def setDisplayer(self, displayer):
		self.displayer = displayer

	def updateAlarm(self, curTime):
		# 0.1 sec for the running time outside the AI module
		if curTime - self.lastTime > timeLimit + 0.1:
			self.over = True
		else:
			self.lastTime = curTime

	def start(self):
        #insert 2 random tiles
		for i in xrange(self.initTiles):
			self.insertRandonTile()

		# show the initial grid state
		# self.displayer.display(self.grid)

		#player plays first
		turn = PLAYER_TURN
		maxTile = 0

		# set init alarm
		self.lastTime = time.clock()

		# check game over conditions
		while not self.isGameOver() and not self.over:
            # make a copy make sure AI cannot change the real grid and cheat
			gridCopy = self.grid.clone()
			move = None

			if turn == PLAYER_TURN:
				# print "Player's Turn"
				move = self.playerAI.getMove(gridCopy)
				# print actionDic[move]

				#validate move
				if move != None and move >= 0 and move < 4:
					if self.grid.canMove([move]):
						self.grid.move(move)
						#update maxTile
						maxTile = self.grid.getMaxTile()
					else:
						print "Invalid PlayerAI Move"
						self.over = True
				else:
					print "Invalid PlayerAI Move - 1"
					self.over = True
			else:
				# print "Computer's turn"
				move = self.computerAI.getMove(gridCopy)
				#validate move
				if move and self.grid.canInsert(move):
					self.grid.setCellValue(move, self.getNewTileValue())
				else:
					print "Invalid Computer AI Move"
					self.over = True

			# if not self.over:
			# 	self.displayer.display(self.grid)

			# once you exceeds the time limit, previous action will be your last action
			self.updateAlarm(time.clock())
			turn = 1 - turn
		# print maxTile
                return maxTile


	def isGameOver(self):
		return not self.grid.canMove()

	def getNewTileValue(self):
		if randint(0,99) < 100 * self.possibility: 
			return self.possibleNewTileValue[0] 
		else: 
			return self.possibleNewTileValue[1];

	def insertRandonTile(self):
		tileValue = self.getNewTileValue()
		cells = self.grid.getAvailableCells()
		cell = cells[randint(0, len(cells) - 1)]
		self.grid.setCellValue(cell, tileValue)


def main():
	gameManager = GameManager()
	playerAI  	= PlayerAI()
	computerAI  = ComputerAI()
	displayer 	= Displayer()
	#set AIs and displayer
	gameManager.setDisplayer(displayer)
	gameManager.setPlayerAI(playerAI)
	gameManager.setComputerAI(computerAI)
	# start the game!
	return gameManager.start()


if __name__ == '__main__':
    trials = 10

    results = {32: 0, 64: 0, 128: 0, 256: 0, 512: 0, 1024: 0, 2048: 0, 4096: 0, 8192: 0}

    for i in xrange(trials):
        result = main()

        gc.collect()

        while result >= 32:
            results[result] += 1

            result /= 2

        if i % 1 == 0:
            print '-'

    results = {key: value * 1.0 / trials for key, value in results.items()}

    pprint(results, width = 1)
