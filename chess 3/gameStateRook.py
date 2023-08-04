from gameStatePiece import *

class GameStateRook(GameStatePiece):
    def __init__(self, color, type, hasMoved, coords):
        super().__init__(color, type, hasMoved, coords)
        self.value = 5

    def getPossibleMoves(self):
        moves = []
        deltasL = [(0,1),(0,-1),(-1,0),(1,0)]
        for deltas in deltasL:
            done = False
            i = 1
            while done == False:
                deltas2 = (deltas[0]*i, deltas[1]*i)
                move = self.createMove(deltas2)
                if move.isValid():
                    moves.append(move)
                    if move.isCapture():
                        done = True
                else:
                    done = True
                i+= 1
        
        return moves
    
