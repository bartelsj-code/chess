from gameStateEmpty import GameStateEmpty
from gameStatePawn import GameStatePawn
from gameStateKnight import GameStateKnight
from gameStateBishop import GameStateBishop
from gameStateRook import GameStateRook
from gameStateQueen import GameStateQueen
from gameStateKing import GameStateKing

def convertToGSPiece(piece, coords):
    type = piece.getType()
    if type != "EMPTY":
        color, hasMoved = piece.getColor(), piece.hasMoved
        if type == "P":
            return GameStatePawn(color, type, hasMoved, coords)
        elif type == "N":
            return GameStateKnight(color, type, hasMoved, coords)
        elif type == "B":
            return GameStateBishop(color, type, hasMoved, coords)
        elif type == "R":
            return GameStateRook(color, type, hasMoved, coords)
        elif type == "Q":
            return GameStateQueen(color, type, hasMoved, coords)
        elif type == "K":
            return GameStateKing(color, type, hasMoved, coords)
    else:
        return GameStateEmpty()