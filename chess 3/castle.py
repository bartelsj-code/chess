from move import Move
class Castle(Move):
    def __init__(self, king, deltas, rook, deltas2):
        super().__init__(king, deltas)
        self.isCastle = True
        self.rook = rook
        self.rookDeltas = deltas2

    def getRookCoords(self):
        return self.rook.getCoords(), self.rookDeltas