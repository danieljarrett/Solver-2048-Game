#!/usr/bin/env python
#coding:utf-8

from BaseAI import BaseAI
from timer  import TimeoutException, setTimer
from Eval   import eval

POSINF = float('inf')
NEGINF = float('-inf')

class PlayerAI(BaseAI):

##############################################################################
# GET MOVE
# Performs iterative-deepening minimax until alloted time runs out
##############################################################################

    def getMove(self, grid):
        depth = 1

        setTimer(0.95)

        try:
            while True:
                move, _ = self.maximize(grid, depth)

                depth += 1

        except TimeoutException:
            pass

        else:
            setTimer(0)

        return move

    # def getMove(self, grid):
    #     move, _ = self.maximize(grid, 1)
    #
    #     return move

##############################################################################
# MAXIMIZE
# Performs maximizing part of minimax by recursively calling minimize
##############################################################################

    def maximize(self, grid, depth):
        moves = grid.getAvailableMoves()
        move, util = None, NEGINF

        if not moves or not depth:
            return None, eval(grid, not moves)

        for newMove in moves:
            newGrid = self.permuteMax(grid, newMove)
            _, newUtil = self.minimize(newGrid, depth - 1)

            if newUtil > util:
                move, util = newMove, newUtil

        return move, util

##############################################################################
# MINIMIZE
# Performs minimizing part of minimax by recursively calling maximize
##############################################################################

    def minimize(self, grid, depth):
        if not depth:
            return None, eval(grid, False)

        moves = grid.getAvailableCells()
        move, util = None, POSINF

        for newCell in moves:
            for tile in [2, 4]:
                newGrid = self.permuteMin(grid, newCell, tile)
                _, newUtil = self.maximize(newGrid, depth - 1)

                if newUtil < util:
                    move, util = newCell, newUtil

        return move, util

##############################################################################
# PERMUTE GRID
# Returns permutations corresponding to maximize or minimize levels
##############################################################################

    def permuteMax(self, grid, move):
        newGrid = grid.clone()
        newGrid.move(move)

        return newGrid

    def permuteMin(self, grid, move, tile):
        newGrid = grid.clone()
        newGrid.setCellValue(move, tile)

        return newGrid
