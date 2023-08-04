from move import Move
class GameStatePiece:
    def __init__(self, color, type, hasMoved, coords):
        self.coords = coords
        self.color = color
        self.type = type
        self.hasMoved = hasMoved

    def getAdvancement(self):
        return self.coords[1]

    def adjustValue(self, amount):
        self.setValue(self.getValue()+amount)

    def setValue(self, amount):
        self.value += amount

    def setHasMoved(self, bool):
        self.hasMoved = bool

    def getValue(self):
        return self.value

    def displayType(self):
        return self.getType()

    def setGrid(self, grid):
        self.grid = grid

    def createMove(self, deltas):
        move = Move(self, deltas)
        move.checkIfValidDestination()
        return move

    def getGrid(self):
        return self.grid

    def setCoords(self, coords):
        self.coords = coords

    def getCoords(self):
        return self.coords

    def getColor(self):
        return self.color

    def notEmpty(self):
        if self.getType() != "EMPTY":
            return True
        else:
            return False

    def getType(self):
        return self.type

    def getPossibleMoves(self):
        pass #done in subclass

    def checkSquareForPiece(self, deltas, types, searchColor):
        coords = self.findNewCoords(deltas)
        if self.squareWithinBounds(coords):
            piece = self.grid[coords[0]][coords[1]]
            if piece.notEmpty():
                if piece.getColor() != searchColor:
                    if piece.getType() in types:
                        return True
        return False

    def checkKnightThreats(self, searchColor):
        found = 0
        deltasL = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for deltas in deltasL:
            if self.checkSquareForPiece(deltas, ["N"], searchColor):
                found += 1
        return found

    def checkKingThreats(self, searchColor):
        found = 0
        deltasL = [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1)]
        for deltas in deltasL:
            if self.checkSquareForPiece(deltas, ["K"], searchColor):
                found += 1
        return found

    def checkPawnThreats(self, searchColor):
        found = 0
        deltasL = [(-1,1),(1,1)]
        for deltas in deltasL:
            if self.checkSquareForPiece(deltas, ["P"], searchColor):
                found += 1
        return found

    def checkDiagonalThreats(self, searchColor):
        found = 0
        deltasL = [(1,1),(-1,-1),(-1,1),(1,-1)]
        for deltas in deltasL:
            done = False
            i = 1
            while done == False:
                deltas2 = (deltas[0]*i, deltas[1]*i)
                if self.checkSquareForPiece(deltas2, ["Q", "B"], searchColor):
                    found += 1
                else:
                    if self.checkSquareUnavaliable(deltas2):
                        done = True
                i += 1
        return found

    def checkOrthogonalThreats(self, searchColor):
        found = 0
        deltasL = [(0,1),(0,-1),(-1,0),(1,0)]
        for deltas in deltasL:
            done = False
            i = 1
            while done == False:
                deltas2 = (deltas[0]*i, deltas[1]*i)
                if self.checkSquareForPiece(deltas2, ["Q", "R"], searchColor):
                    found +=1
                else:
                    if self.checkSquareUnavaliable(deltas2):
                        done = True
                i += 1
        return found

    def checkSquareUnavaliable(self, deltas):
        coords = self.findNewCoords(deltas)
        if self.squareWithinBounds(coords):
            if self.grid[coords[0]][coords[1]].notEmpty():
                return True
            return False
        return True

    def findNewCoords(self, deltas):
        x = self.coords[0] + deltas[0]
        y = self.coords[1] + deltas[1]
        return (x, y)

    def withinBounds(self, number):
        if number >= 0 and number <= 7:
            return True
        else:
            return False

    def squareWithinBounds(self, coords):
        if self.withinBounds(coords[0]) and self.withinBounds(coords[1]):
            return True
        else:
            return False

    # def countThreats(self):
    #     a = self.checkKnightThreats()
    #     b = self.checkDiagonalThreats()
    #     c = self.checkOrthogonalThreats()
    #     d = self.checkPawnThreats()
    #     e = self.checkKingThreats()
    #     return a + b + c + d + e
    def getOppositeColor(self):
        if self.color == "W":
            return "B"
        else:
            return "W"

    def threatExists(self):
        compareColor = self.getColor()
        checks = [self.checkDiagonalThreats,\
                self.checkOrthogonalThreats,\
                self.checkKnightThreats,\
                self.checkPawnThreats, \
                self.checkKingThreats,]
        for check in checks:
            if check(compareColor) != 0:
                return True
        return False


    def isDefended(self):
        compareColor = self.getOppositeColor()
        # Works for opposing color in gamestate, not for the primary
        checks = [self.checkPawnThreats, \
            self.checkDiagonalThreats,\
            self.checkKnightThreats,\
            self.checkOrthogonalThreats,\
            self.checkKingThreats,]
        for check in checks:
            if check(compareColor) != 0:
                return True
        return False
