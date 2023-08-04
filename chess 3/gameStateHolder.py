from gameState import GameState

class GameStateHolder:
    def __init__(self, gameState, move): 
        self.movesGenerated = False
        self.gameState = gameState
        self.color = self.gameState.color
        self.evaluatedChildren = []
        self.eval = 0
        self.priorMove = move
        self.unevaluatedMoves = []

    def __repr__(self):
        return self.priorMove.toString()

    def generateMoves(self):
        self.unevaluatedMoves = self.gameState.getAllPossibleMoves()
        self.movesGenerated = True

    def sortChildren(self):
        if self.color == "W":
            self.evaluatedChildren.sort(key=lambda x: x.eval, reverse=True)
        else:
            self.evaluatedChildren.sort(key=lambda x: x.eval)





