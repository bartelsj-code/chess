from piece import *
class Empty(Piece):
    def __init__(self):
        self.type = "EMPTY"
        self.shape = []
        self.color = None
        pass
    
    def getShorthand(self):
        return "  "

    def getColor(self):
        return self.color