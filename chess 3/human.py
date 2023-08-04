from graphics import *
from gameState import GameState
from player import Player
from pieceSelectionWindow import PieceSelectionWindow

class Human(Player):
    def __init__(self, color, board, win):
        super().__init__(color, board)
        self.win = win

    def doTurn(self, lastMove):
        startingGS = self.board.exportAsGameState(self.color)
        notDone = True
        moves = self.getPossibleMoves(startingGS)
        while notDone:
            start = self.board.viewCoordsToBoardCoords(self.color, self.board.getCoordsFromPoint(self.win.getMouse()))
            end = self.board.viewCoordsToBoardCoords(self.color, self.board.getCoordsFromPoint(self.win.getMouse()))
            possibleMoves = []
            for move in moves:
                moveCoords = move.getSquaresCoords()
                if moveCoords[0] == start and moveCoords[1] == end:
                    possibleMoves.append(move)
            if len(possibleMoves) == 1:
                self.doMoveSequence(possibleMoves[0])
                return possibleMoves[0]
            elif len(possibleMoves) != 0:
                type = self.getPromotionType()
                for move in possibleMoves:
                    if move.promotionPiece.getType() == type:
                        self.doMoveSequence(move)
                        return move
        
    def getPromotionType(self):
        pieceSelectionWindow = PieceSelectionWindow(self.color)
        pieceSelectionWindow.fill()
        type = pieceSelectionWindow.getType()
        pieceSelectionWindow.close()
        return type

    