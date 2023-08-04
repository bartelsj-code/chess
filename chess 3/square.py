from empty import Empty
from graphics import *
import math

class Square:
    def __init__(self, name, coords, sdi):
        self.placeHolder = Empty()
        self.name = name
        self.occupant = self.placeHolder
        self.coords = coords
        self.sdi = sdi
        self.win = sdi.getWin()
        self.centerCoords = (0,0)
        self.rect = self.makeRect(sdi)
        self.text = self.makeText(sdi)

    def makeRect(self, sdi):
        location = sdi.getLocation()
        self.size = sdi.getSize()
        color = sdi.getColor()
        x1, y1 = location[0], location[1]
        x2, y2 = x1 + self.size, y1 + self.size
        self.centerCoords = ((x1+(x2-x1)/2),(y1+(y2-y1)/2))
        p1 = Point(x1,y1)
        p2 = Point(x2,y2)
        rect = Rectangle(p1, p2)
        rect.setFill(color)
        rect.setWidth(0)
        return rect

    def makeText(self, sdi):
        location = sdi.getLocation()
        self.size = sdi.getSize()
        color = sdi.getIC()
        x1, y1 = location[0]+ 0.12*self.size, location[1] + 0.88*self.size
        p1 = Point(x1,y1)
        text = Text(p1, self.name)
        text.setSize(int(self.size)//7)
        text.setTextColor(color)
        return text

    def getScalingUnit(self):
        return self.size

    def draw(self):
        self.rect.draw(self.win)
        self.text.draw(self.win)

    def getCenterCoords(self):
        return self.centerCoords

    def getCoords(self):
        return self.coords

    def getName(self):
        return self.name

    def getOccupant(self):
        return self.occupant

    def setOccupant(self, piece):
        self.occupant.undraw()
        self.occupant = piece
    
    def clearOccupant(self):
        self.occupant = self.placeHolder

    def highlight(self):
        self.rect.setFill(self.sdi.hl)

    def normalize(self):
        self.rect.setFill(self.sdi.getColor())

