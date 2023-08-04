from gameStatePiece import *

class GameStateKnight(GameStatePiece):
    def __init__(self, color, type, hasMoved, coords):
        super().__init__(color, type, hasMoved, coords)
        self.value = 3
    
    def getPossibleMoves(self):
        moves = []
        deltasL = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for deltas in deltasL:
            move = self.createMove(deltas)
            if move.isValid():
                moves.append(move)
        return moves
