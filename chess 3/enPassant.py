from move import Move
class EnPassant(Move):
    def __init__(self, pawn, deltas):
        super().__init__(pawn, deltas)
        self.endDeltas = (deltas[0], deltas[1]+1)
        self.isEnPassant = True

    def getEndCoords(self):
        return (self.newX, self.newY+1)
    
    def getUniCoords(self):
        x = self.newX
        y = self.newY+1
        if self.piece.color == "B":
            x, y = 7-x, 7-y
        return x, y
    
    def getSquareName(self):
        x, y = self.getUniCoords()
        str1 = chr(x + 97)
        str2 = str(y + 1)
        return str1+str2
