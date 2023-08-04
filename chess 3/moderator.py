from player import Player
class Moderator(Player):
    def __init__(self, board):
        super().__init__("W", board)
        self.positionsDict = {}

    def testForMate(self, lastPlayer):
        gs = self.getGameStateFromBoard()
        gs2 = self.flipToMatch(gs, lastPlayer)
        if self.threeReps(gs):
            return True
        mate = gs2.checkForMate()
        if mate != False:
            return True
        return False

    def flipToMatch(self, gs, player):
        if gs.color == player.color:
            return gs.makeFlip()
        else:
            return gs

    def threeReps(self, gs):
        gs = gs.toString()
        if gs in self.positionsDict:
            self.positionsDict[gs] += 1
        else:
            self.positionsDict[gs] = 1
        if self.positionsDict[gs] == 3:
            return True
        else:
            return False
        


        