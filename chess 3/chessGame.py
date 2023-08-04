from board import Board
from graphics import *
from time import sleep
from human import Human
import engine6
import engine6_5
from moderator import Moderator

class Game:
    def __init__(self, length, view):
        self.win = makeWindow(length)
        self.win.setBackground("dark green")
        self.board = Board(length, 0.5, self.win, view)
        positionFile = "StandardSetup.csv"
        # positionFile = "StandardSetupDisadvantage.csv"
        # positionFile = "test.csv"
        # positionFile = "recorder.csv"
        self.whitePlayer = Human("W", self.board, self.win)
        # self.blackPlayer = Human("B", self.board, self.win)
        # self.whitePlayer = engine6.Engine("W", self.board, 12000)
        self.blackPlayer = engine6.Engine("B", self.board, 2000)
        self.board.setupPositionFromCSV(positionFile)
        self.moderator = Moderator(self.board)

    def play(self):
        players = [self.whitePlayer, self.blackPlayer]
        done = False
        lastmove = None
        while done == False:
            for player in players:
                move = player.doTurn(lastmove)
                lastmove = move
                print(move)
                self.board.writePositionIntoCSV("recorder.csv")
                if self.moderator.testForMate(player):
                    done = True
                    break
        self.win.changeTitle("Game Over")
        x = input("S")

def makeWindow(length):
    return GraphWin("Board", length, length)

if __name__ == "__main__":
    g = Game(900, "W")
    g.play()
