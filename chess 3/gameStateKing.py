from gameStatePiece import *

class GameStateKing(GameStatePiece):
    def __init__(self, color, type, hasMoved, coords):
        super().__init__(color, type, hasMoved, coords)
        self.value = 0.1

    def getPossibleMoves(self):
        moves = []
        deltasL = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
        for deltas in deltasL:
            move = self.createMove(deltas)
            if move.isValid():
                moves.append(move)
        return moves

    def isInCheck(self):
        if self.checkForChecks():
            return True
        else:
            return False

    def checkForChecks(self):
        if self.threatExists():
            return True
        return False

    

    