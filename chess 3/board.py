import math
import csv
from gameState import GameState

from pawn import Pawn
from knight import Knight
from bishop import Bishop
from rook import Rook
from king import King
from queen import Queen

from gameStateConversion import *
from squareDrawInfo import SquareDrawInfo
from square import Square
from graphics import *

class Board:
    def __init__(self, length, borderInSquares, win, view):
        self.activePlayer = "White"
        self.view = view
        self.win = win
        self.length = length
        self.squareLength = length/(borderInSquares*2 + 8)
        self.borderWidth = self.squareLength*borderInSquares
        self.squaresLst = self.makeSquares()
        self.pieces = []
        self.highlighted = []

    def makePiece(self, color, type, square):
        if type == "P":
            piece = Pawn(color, square, self.win)
        elif type == "R":
            piece = Rook(color, square, self.win)
        elif type == "N":
            piece = Knight(color, square, self.win)
        elif type == "B":
            piece = Bishop(color, square, self.win)
        elif type == "Q":
            piece = Queen(color, square, self.win)
        elif type == "K":
            piece = King(color, square, self.win)
        return piece
        
    def makePieces(self, sourceList):
        for y in range(8):
            for x in range(8):
                shorthand = sourceList[x][y]
                if shorthand != '__':
                    color = shorthand[0]
                    type = shorthand[1]
                    square = self.squaresLst[x][y]
                    piece = self.makePiece(color, type, square)
                    self.pieces.append(piece)

    def promote(self, square, promotionType):
        currentOccupant = square.getOccupant()
        if promotionType == "N":
            
            replacement = Knight(currentOccupant.getColor(), square, self.win)
        elif promotionType == "B":

            replacement = Bishop(currentOccupant.getColor(), square, self.win)
        elif promotionType == "R":

            replacement = Rook(currentOccupant.getColor(), square, self.win)
        elif promotionType == "Q":

            replacement = Queen(currentOccupant.getColor(), square, self.win)
        
        self.pieces.remove(currentOccupant)
        self.pieces.append(replacement)
        square.setOccupant(replacement)
        currentOccupant.undraw()
        replacement.draw()

    def switchActive(self):
        if self.activePlayer == "White":
            self.activePlayer = "Black"    
        else:
            self.activePlayer = "White"    

    def drawPieces(self):
        for piece in self.pieces:
            piece.draw()

    def doMove(self, selectSquare, destinationSquare):
        if selectSquare.getOccupant().getType() != "EMPTY":
            selectSquare.getOccupant().makeMove(destinationSquare)
        self.switchActive()
        self.win.changeTitle("{}'s Turn".format(self.activePlayer))
        self.highlightSquares(selectSquare, destinationSquare)

    def highlightSquares(self, square1, square2):
        for square in self.highlighted:
            square.normalize()
        self.highlighted = []
        self.highlighted.append(square1)
        self.highlighted.append(square2)
        for square in self.highlighted:
            square.highlight()

    def showInConsole(self, focus):
        line = ""
        for i in range(8):
            line += "|"
            for j in range(8):
                if focus == "pieces":
                    line += self.squaresLst[i][j].getOccupant().getShorthand() + "|"
                if focus == "squares":
                    line += self.squaresLst[i][j].getName() + "|"
            line += '\n'
        print(line)

    def makeSquares(self):
        namesList = makeNamesList()
        squares = [[],[],[],[],[],[],[],[]]
        c = 0
        c2 = 1
        for i in range(8):
            for j in range(8):
                name = namesList[c]
                if c2 % 2 == 0:
                    color = color_rgb(55,35,35)
                    hl = color_rgb(80,56,30)
                    ic = color_rgb(180,180,180)
                else:
                    ic = color_rgb(55,35,35)
                    hl = color_rgb(212,212,160)
                    color = color_rgb(180,180,180)
                if self.view == 'W':
                    x = j * self.squareLength + self.borderWidth
                    y = i * self.squareLength + self.borderWidth
                if self.view == 'B':
                    windowLength = 2*self.borderWidth+8*self.squareLength
                    x = windowLength-(j * self.squareLength + self.borderWidth + self.squareLength)
                    y = windowLength-(i * self.squareLength + self.borderWidth + self.squareLength)
                sdi = SquareDrawInfo(color, ic, hl, self.squareLength, (x,y), self.win)
                square = Square(name, (i,j), sdi)
                square.draw()
                squares[i].append(square)
                c += 1
                c2 +=1
            c2 += 1
        return squares

    def getCoordsFromPoint(self, point):
        x = math.floor((point.getX() - self.borderWidth)/self.squareLength)
        y = math.floor((point.getY() - self.borderWidth)/self.squareLength)
        return (x,y)

    def getSquareFromCoordsView(self, coords):
        x = coords[0]
        y = coords[1]
        if self.view == "W":
            square = self.squaresLst[y][x]
        else:
            square = self.squaresLst[7-y][7-x]
        return square

    def getSquareFromCoordsColor(self, color, coords):
        x = coords[0]
        y = coords[1]
        if color == "W":
            square = self.squaresLst[7-y][x]
        else:
            square = self.squaresLst[y][7-x]
        return square

    def viewCoordsToBoardCoords(self, color, coords):
        x = coords[0]
        y = coords[1]
        if color == "W":
            if self.view == "W":
                coords = (x, 7-y)
            else:
                coords = (7-x, y)
        else:
            if self.view == "B":
                coords = (x, 7-y)
            else:
                coords = (7-x, y)
            
        return coords

    def exportAsGameState(self, color):
        squareGrid = self.squareGridFromColor(color)
        gameState = GameState(color)
        gameState.copyBoard(squareGrid)
        return gameState
        
    def squareGridFromColor(self, color):
        sqrslst = []
        if color == "W":
            for i in range(8):
                row = []
                for j in range(7,-1,-1):
                    row.append(self.squaresLst[j][i])
                sqrslst.append(row)
        else:
            for i in range(7,-1,-1):
                row = []
                for j in range(8):
                    row.append(self.squaresLst[j][i])
                sqrslst.append(row)
        return(sqrslst)   

    def writePositionIntoCSV(self, fileName):
        with open(fileName, 'w', newline = '') as destinationFile:
            writer = csv.writer(destinationFile, delimiter=',')
            for y in range(8):
                row = []
                for x in range(8):
                    square = self.squaresLst[y][x]
                    occupant = square.getOccupant()
                    if occupant.getType() != "EMPTY":
                        shorthand = occupant.getShorthand()
                    else:
                        shorthand = '__'
                    row.append(shorthand)
                writer.writerow(row)
        destinationFile.close()
                    
    def setupPositionFromCSV(self, fileName):
        with open(fileName, 'r') as sourceFile:
            basicGrid = csv.reader(sourceFile)
            sourceList = []
            for row in basicGrid:
                sourceList.append(row)
            self.makePieces(sourceList)
            self.drawPieces()
        sourceFile.close()
                    
def makeNamesList():
    lst = []
    letters = ['a','b','c','d','e','f','g','h']
    for i in range(8,0,-1):
        for j in range(8):
            letter = letters[j]
            number = str(i)
            name = letter + number
            lst.append(name)
    return lst

