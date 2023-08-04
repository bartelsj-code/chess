from gameStatePiece import *
from gameStateRook import GameStateRook
from gameStateQueen import GameStateQueen
from gameStateBishop import GameStateBishop
from gameStateKnight import GameStateKnight
from enPassant import EnPassant

class GameStatePawn(GameStatePiece):
    def __init__(self, color, type, hasMoved, coords):
        super().__init__(color, type, hasMoved, coords)
        self.value = 1
        self.justDoubleMoved = False

    def setDoubleMoved(self):
        self.justDoubleMoved = True
    
    def getPossibleMoves(self):
        allMoves = []
        if self.coords[1] == 6:
            knight = GameStateKnight(self.color, "N", True, self.coords)
            bishop = GameStateBishop(self.color, "B", True, self.coords)
            rook = GameStateRook(self.color, "R", True, self.coords)
            queen = GameStateQueen(self.color, "Q", True, self.coords)
            replacements = [knight, bishop, rook, queen]
            for replacement in replacements:
                moveSet = self.findPossible()
                for move in moveSet:
                    move.setPromotion(replacement)
                    allMoves.append(move)       
        else:
            allMoves = self.findPossible()
            if self.coords[1] == 4:
                #a peasant
                deltasL = [(1,0), (-1,0)]
                for deltas in deltasL:
                    move = self.createEnPassant(deltas)
                    if move.isCapture():
                        if move.captureType == "P":
                            if move.capturePiece.justDoubleMoved == True:
                                allMoves.append(move)    

        return allMoves

    def findPossible(self):
        moves = []
        move = self.createMove((0,1))
        if move.isValid() and move.isCapture() == False:
            moves.append(move)
            if self.coords[1] == 1:
                move = self.createMove((0,2))
                if move.isValid() and move.isCapture() == False:
                    move.setDoublePush()
                    moves.append(move)
                    
        deltasL = [(1,1), (-1,1)]
        for deltas in deltasL:
            move = self.createMove(deltas)
            if move.isCapture():
                moves.append(move)           
        return moves
    
    def createEnPassant(self, deltas):
        move = EnPassant(self, deltas)
        move.checkIfValidDestination()
        return move
    