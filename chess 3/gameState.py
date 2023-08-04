from castle import Castle
from gameStateConversion import *
from gameStateEmpty import GameStateEmpty
from gameStatePiece import GameStatePiece
import random

class GameState:
    def __init__(self, color):
        self.movesAssigned = False
        self.color = color
        self.ownKing = None
        self.opponentKing = None

    def toString(self):
        summary = ""
        summary += self.color
        for piece in self.allPieces:
            pieceString1 = piece.color + piece.type + str(piece.coords[0])
            if piece.hasMoved == True:
                pieceString1 += "H"
            pieceString1 += str(piece.coords[1])
            summary += pieceString1
        return summary

    def getColor(self):
        return self.color

    def copyBoard(self, layout):
        self.boardToGrid(layout)
        self.assignPieces()
        self.givePiecesGrid()

    def getPieces(self):
        return self.allPieces

    def givePiecesGrid(self):
        for piece in self.friendPieces:
            piece.setGrid(self.grid)

    def getSquareFromUniCoords(self, x, y):
        if self.color == "B":
            x, y = 7-x, 7-y
        return self.grid[x][y]

    def assignPieces(self):
        self.friendPieces = []
        self.enemyPieces = []
        self.friendPawns = []
        self.enemyPawns = []
        for i in range(8):
            for j in range(8):
                if self.grid[j][i].notEmpty():
                    if self.color == self.grid[j][i].getColor():
                        if self.grid[j][i].getType() == "K":
                            self.ownKing = self.grid[j][i]
                        elif self.grid[j][i].getType() == "P":
                            self.friendPawns.append(self.grid[j][i])
                        self.friendPieces.append(self.grid[j][i])
                    else:
                        if self.grid[j][i].getType() == "K":
                            self.opponentKing = self.grid[j][i]
                        elif self.grid[j][i].getType() == "P":
                            self.enemyPawns.append(self.grid[j][i])
                        self.enemyPieces.append(self.grid[j][i])
        self.allPieces = self.friendPieces + self.enemyPieces
        
        if self.color == "W":
            self.whiteKing = self.ownKing
            self.blackKing = self.opponentKing
            self.whitePieces = self.friendPieces
            self.blackPieces = self.enemyPieces
        else:
            self.whiteKing = self.opponentKing
            self.blackKing = self.ownKing
            self.whitePieces = self.enemyPieces
            self.blackPieces = self.friendPieces

    def makeClone(self):
        gameState = GameState(self.color)
        gameState.cloneCopy(self.grid)
        return gameState

    def makeFlip(self):
        gameState = GameState(self.getOpposite(self.color))
        gameState.flipCopy(self.grid)
        return gameState

    def cloneCopy(self, grid):
        self.gridToGrid(grid)
        self.assignPieces()
        self.givePiecesGrid()   
        
    def flipCopy(self, grid):
        self.gridToFlipGrid(grid)
        self.assignPieces()
        self.givePiecesGrid()

    def flipWithMove(self, move):
        return self.cloneWithMove(move).makeFlip()

    def cloneWithMove(self, move):
        gameState = self.makeClone()
        startCoords, endCoords = move.getSquaresCoords()
        gameState.adjustGridForMove(startCoords, endCoords)
        if move.doublePush:
            gameState.markDouble(endCoords)
        if move.isPromotion:
            gameState.promote(endCoords, move.promotionPiece)
        if move.isCastle:
            coords1, coords2 = move.getRookCoords()
            gameState.adjustGridForMove(coords1, coords2)
        if move.isEnPassant:
            finalCoords = move.getEndCoords()
            gameState.adjustGridForMove(endCoords, finalCoords)
        return gameState
    
    def markDouble(self, coords):
        self.grid[coords[0]][coords[1]].setDoubleMoved()

    def promote(self, coords, replacement):
        self.allPieces.remove(self.grid[coords[0]][coords[1]])
        self.grid[coords[0]][coords[1]] = replacement
        self.allPieces.append(replacement)
        self.friendPieces.append(replacement)

    def adjustGridForMove(self, start, end):
        self.grid[start[0]][start[1]].setHasMoved(True)
        if self.grid[end[0]][end[1]] in self.allPieces:
            self.allPieces.remove(self.grid[end[0]][end[1]])
        self.grid[end[0]][end[1]] = self.grid[start[0]][start[1]]
        self.grid[start[0]][start[1]] = GameStateEmpty()
        self.grid[end[0]][end[1]].setCoords((end[0],end[1]))

    def getAllMoves(self):
        allMoves = []
        for piece in self.friendPieces:
            moves = piece.getPossibleMoves()
            allMoves += moves
        allMoves += self.findCastles()
        return allMoves
        
    def getAllPossibleMoves(self):
        if self.movesAssigned == False:
            self.movesAssigned = True
        else:
            return self.legalMoves
        allMoves = []
        for piece in self.friendPieces:
            moves = piece.getPossibleMoves()

            allMoves += moves
        allMoves += self.findCastles()
        self.allMoves = allMoves
        legalMoves = []
        for move in allMoves:
            adjustedBoard = self.cloneWithMove(move)
            if adjustedBoard.notInCheck():
                legalMoves.append(move)
        self.legalMoves = legalMoves
        self.movesLength = len(self.legalMoves)
        return legalMoves

    def checkForMate(self):
        moves = self.getAllPossibleMoves()
        if self.movesLength == 0:
            if self.isInCheck():
                return "Checkmate"
            else:
                return "Stalemate"
        return False

    def findCastles(self):
        castles = []
        king = self.findKing()
        if self.notInCheck():
            if king.hasMoved == False:
                coords = king.getCoords()
                rook1 = self.grid[0][0]
                knight1 = self.grid[1][0]
                rook2 = self.grid[7][0]
                knight2 = self.grid[6][0]
                if rook1.getType() == "R" and rook1.hasMoved == False and knight1.getType() == "EMPTY":
                    if self.checkNeighbors(-1, coords):
                        castle = Castle(king, (-2,0), rook1, (coords[0]-1, coords[1]))
                        castles.append(castle)
                if rook2.getType() == "R" and rook2.hasMoved == False and knight2.getType() == "EMPTY":
                    if self.checkNeighbors(1, coords):
                        castle = Castle(king, (2,0), rook2, (coords[0]+1, coords[1]))
                        castles.append(castle)
        return castles

    def checkNeighbors(self, direction, coords):
        neighbor1Coords = (coords[0] + direction,coords[1])
        neighbor2Coords = (coords[0] + direction * 2,coords[1])
        neighbor1 = self.grid[neighbor1Coords[0]][neighbor1Coords[1]]
        neighbor2 = self.grid[neighbor2Coords[0]][neighbor2Coords[1]]
        if neighbor1.notEmpty() == False:
            if self.isSafe(neighbor1, neighbor1Coords):
                if neighbor2.notEmpty() == False:
                    if self.isSafe(neighbor2, neighbor2Coords):
                        return True
        return False

    def isSafe(self, neighbor, coords):
        neighbor.giveGrid(self.grid)
        neighbor.giveCoords(coords)
        neighbor.giveColor(self.color)
        if neighbor.threatExists():
            neighbor.removeColor()
            return False
        else:
            neighbor.removeColor()
            return True          
                
    def gridToGrid(self, grid):
        self.grid = self.makeGrid()
        for i in range(8):
            for j in range(8):
                newPiece = convertToGSPiece(grid[j][i], (j,i))
                self.grid[j][i] = newPiece

    def gridToFlipGrid(self, grid):
        self.grid = self.makeGrid()
        for i in range(8):
            for j in range(8):
                newPiece = convertToGSPiece(grid[j][i], (7-j,7-i))
                self.grid[7-j][7-i] = newPiece

    def boardToGrid(self, layout):
        self.grid = self.makeGrid()
        for i in range(8):
            for j in range(8):
                newPiece = convertToGSPiece(layout[j][i].getOccupant(), (j,i))
                self.grid[j][i] = newPiece

    def display(self):
        for i in range(8):
            ln = "|"
            for j in range(8):
                ln += self.grid[j][i].getColor() + self.grid[j][i].displayType() + "|"
            print(ln)
        print()

    def getMaterial(self):
        whiteMaterial = 0
        blackMaterial = 0
        for piece in self.allPieces:
            if piece.getType() != "K":
                if piece.getColor() == 'W':
                    whiteMaterial += piece.getValue()
                else:
                    blackMaterial += piece.getValue()
        return whiteMaterial, blackMaterial

    def getPieceCount(self):
        return len(self.allPieces)

    def getColor(self):
        return self.color

    def findKing(self):
        return self.ownKing
        
    def notInCheck(self):
        try:
            king = self.findKing()
            if king.isInCheck():
                return False
            else:
                return True
        except:
            self.display()
            king = self.findKing()
            if king.isInCheck():
                return False
            else:
                return True

    def isInCheck(self):
        if self.notInCheck():
            return False
        else:
            return True

    def getOpposite(self, color):
        if color == "B":
            return "W"
        else:
            return "B"
            
    def makeGrid(self):
        grid = [[None,None,None,None,None,None,None,None],\
                [None,None,None,None,None,None,None,None],\
                [None,None,None,None,None,None,None,None],\
                [None,None,None,None,None,None,None,None],\
                [None,None,None,None,None,None,None,None],\
                [None,None,None,None,None,None,None,None],\
                [None,None,None,None,None,None,None,None],\
                [None,None,None,None,None,None,None,None]]
        return grid

