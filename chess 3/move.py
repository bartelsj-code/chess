class Move:
    def __init__(self, piece, deltas):
        self.grid = piece.getGrid()
        self.piece = piece
        self.dy = deltas[1]
        self.dx = deltas[0]
        self.x = self.piece.getCoords()[0]
        self.y = self.piece.getCoords()[1]
        self.valid = True
        self.isCap = False
        self.setDestinationSquare()
        self.isPromotion = False
        self.isEnPassant = False
        self.isCastle = False
        self.doublePush = False
    
    def setDoublePush(self):
        self.doublePush = True

    def setPromotion(self, replacement):
        self.isPromotion = True
        self.promotionPiece = replacement

    def isValid(self):
        return self.valid

    def setDestinationSquare(self):
        self.newX = self.x + self.dx
        self.newY = self.y + self.dy
        if self.outOfBounds(self.newX) or self.outOfBounds(self.newY):
            self.valid = False
            self.destinationSquare = None
        else:    
            self.destinationSquare = self.grid[self.newX][self.newY]

    def getDestinationSquare(self):
        return self.destinationSquare

    def isCapture(self):
        return self.isCap

    def getSquaresCoords(self):
        return (self.x, self.y), (self.newX, self.newY)

    def outOfBounds(self, newVal):
        if newVal < 0 or newVal > 7:
            return True
        else:
            return False

    def toString(self):
        str = ""
        if self.piece.getType() != "P":
            str += self.piece.getType()
        if self.isCap:
            str += "x"
        str += self.getSquareName()
        if self.isPromotion:
            str += "={}".format(self.promotionPiece.getType())
        return str

    def getUniCoords(self):
        x = self.newX
        y = self.newY
        if self.piece.color == "B":
            x, y = 7-x, 7-y
        return x, y

    def getSquareName(self):
        x, y = self.getUniCoords()
        str1 = chr(x + 97)
        str2 = str(y + 1)
        return str1+str2

    def __repr__(self):
        return self.toString()

    def checkIfValidDestination(self):
        if self.destinationSquare == None:
            self.valid = False
        elif self.destinationSquare.getColor() == self.piece.getColor():
            self.valid = False
        elif self.destinationSquare.getType() != "EMPTY":
            self.isCap = True
            self.capturePiece = self.destinationSquare
            self.captureType = self.destinationSquare.getType()
            self.captureValue = self.destinationSquare.getValue()

    






