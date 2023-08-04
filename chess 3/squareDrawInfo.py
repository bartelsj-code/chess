
class SquareDrawInfo:
    def __init__(self, color, ic, hl, size, location, win):
        self.inverseColor = ic
        self.color = color
        self.hl = hl
        self.size = size
        self.location = location
        self.win = win

    def getLocation(self):
        return self.location

    def getSize(self):
        return self.size
    
    def getColor(self):
        return self.color

    def getWin(self):
        return self.win

    def getIC(self):
        return self.inverseColor

    