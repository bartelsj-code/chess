from gameStatePiece import *

class GameStateEmpty(GameStatePiece):
    def __init__(self):
        self.type = "EMPTY"
        self.shape = []
        self.color = " "
        pass

    def getColor(self):
        return self.color
    
    def displayType(self):
        return " "

    def giveCoords(self, coords):
        self.coords = coords

    def giveGrid(self, grid):
        self.grid = grid

    def giveColor(self, color):
        self.color = color

    def removeColor(self):
        self.color = " "