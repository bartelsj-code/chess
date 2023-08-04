from graphics import *
from knight import Knight
from bishop import Bishop
from rook import Rook
from queen import Queen

class PieceSelectionWindow:
    def __init__(self, color):
        self.color = color
        self.length = 300
        self.height = 100
        self.win = GraphWin("Promotion Piece Selection", self.length, self.height)
        self.typesDict = {0:"N",1:"B",2:"R",3:"Q"}
    
    def fill(self):
        self.win.setBackground("dark green")
        pieces = self.makePieces()
        for piece in pieces:
            piece.draw()

    def makePieces(self):
        squareLength = self.length // 4
        squareHeight = self.height
        squareList = []
        pieces = []
        for i in range(4):
            squareList.append(SquareReplacement(i*squareLength, squareLength, squareHeight))
        knight = Knight(self.color, squareList[0], self.win)
        pieces.append(knight)
        bishop = Bishop(self.color, squareList[1], self.win)
        pieces.append(bishop)
        rook = Rook(self.color, squareList[2], self.win)
        pieces.append(rook)
        queen = Queen(self.color, squareList[3], self.win)
        pieces.append(queen)
        return pieces

    def getType(self):
        option = self.win.getMouse().getX()//(self.length/4)
        return self.typesDict[option]

    def close(self):
        self.win.close()

class SquareReplacement:
    def __init__(self, x, squareLength, squareHeight):
        self.x = x
        self.scale = squareHeight
        self.squareHeight = squareHeight
        self.squareLength = squareLength
        pass

    def getCenterCoords(self):
        middleX = self.x + self.squareLength / 2
        y = self.squareHeight / 2

        return (middleX, y)

    def setOccupant(self, occupant):
        pass

    def getScalingUnit(self):
        return self.scale

    
