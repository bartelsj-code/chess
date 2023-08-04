from evaluator2 import Evaluator
class Player:
    def __init__(self, color, board):
        self.color = color
        self.board = board
        pass

    def doTurn(self):
        pass

    def getColor(self):
        return self.color
        
    def doMoveSequence(self, move):
        coords1, coords2 = move.getSquaresCoords()
        start = self.board.getSquareFromCoordsColor(self.color, coords1)
        destination = self.board.getSquareFromCoordsColor(self.color, coords2)
        self.board.doMove(start, destination)
        if move.isPromotion:
            self.board.promote(destination, move.promotionPiece.getType())
        if move.isCastle:
            coords1, coords2 = move.getRookCoords()
            start = self.board.getSquareFromCoordsColor(self.color, coords1)
            destination = self.board.getSquareFromCoordsColor(self.color, coords2)
            self.board.doMove(start, destination)
        if move.isEnPassant:
            coords3 = move.getEndCoords()
            end = self.board.getSquareFromCoordsColor(self.color, coords3)
            self.board.doMove(destination, end)

    def getPossibleMoves(self, gameState):
        moves = gameState.getAllPossibleMoves()
        return moves

    def getGameStateFromBoard(self):
        return self.board.exportAsGameState(self.color)