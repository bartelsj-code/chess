from graphics import *
from time import sleep
from math import floor

class Piece:
    def __init__(self, color, type, square, win):
        self.color = color
        self.type = type
        self.setSquare(square)
        self.hasMoved = False
        self.win = win
        self.shape = []
        self.makeShape()
        self.isCaptured = False

    def getCC(self):
        x = self.square.getCenterCoords()[0]
        y = self.square.getCenterCoords()[1]
        scale = self.square.getScalingUnit()
        return x, y, scale

    def capture(self):
        self.isCaptured = True

    def isCaptured(self):
        return self.isCaptured
        
    def makeShape(self):
        pass #in subclasses

    def setSquare(self, square):
        self.square = square
        self.square.setOccupant(self)

    def getColor(self):
        return self.color

    def getType(self):
        return self.type

    def getValue(self):
        return self.value

    def getSquare(self):
        return self.square

    def getShorthand(self):
        shorthand = self.color + self.type
        return shorthand

    def makeMove(self, square):
        x1, y1, scale = self.getCC()
        self.hasMoved = True
        self.square.clearOccupant()
        self.setSquare(square)
        x2, y2, scale = self.getCC()
        self.move((x1,y1),(x2,y2))

    def getColorPair(self):
        if self.color == "W":
            return "white", "black"
        else:
            return "black", "white"

    def draw(self):
        for part in self.shape:
            color, outline = self.getColorPair()
            part.setOutline(outline)
            part.setFill(color)
            part.draw(self.win)

    def undraw(self):
        for part in self.shape:
            part.undraw()

    def calcDeltas(self, loc1, loc2):
        dx = (loc2[0]-loc1[0])
        dy = (loc2[1]-loc1[1])
        return dx, dy

    def move(self, loc1, loc2):
        duration = 0.2
        fps = 40
        frameCount = floor(duration * fps)
        if frameCount == 0:
            frameCount += 1
        delay = duration/frameCount
        dx,dy = self.calcDeltas(loc1, loc2)
        for i in range(frameCount):
            sleep(delay)
            for part in self.shape:
                part.move(dx/frameCount,dy/frameCount)
                



    
