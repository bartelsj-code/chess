import math
class Evaluator:
    def __init__(self):
        self.moves_made = 0
        self.counter = 0
        self.encroachmentLevels = {"P": 0, "N": 1, "B": 0.5, "R": 0, "Q": 0, "K": 0}
        self.encroachmentFactor = 0.002
        self.materialBase = 10
        self.materialLogMultiplier = 1
        self.devFactor = 0.03
        self.pawnFactor = 0.005
        self.oppositionFactor = 0.003
        # self.kingConnectionFactor = 0.001
        self.kingCenterFactor = 0.008
        pass

    def mateOnlyEvaluate(self, gameState):
        mate = gameState.checkForMate()
        if mate:
            return self.mates(mate)
        return 0

    def evaluate(self, gameState):
        self.counter += 1
        finalEval = 0
        mate = gameState.checkForMate()
        if mate != False:
            return self.mates(mate)
        if self.moves_made < 12:
            #opening
            finalEval += self.evaluateMaterial(gameState)
            finalEval += self.getDevelopment(gameState)
        elif self.moves_made < 48:
            finalEval += self.evaluateMaterial(gameState)
            finalEval += self.pawnEvaluate(gameState)
            finalEval += self.kingEncroachment(gameState)
            # finalEval += self.kingOpposition(gameState, finalEval)
        else:
            finalEval += self.evaluateMaterial(gameState)
            finalEval += self.pawnEvaluate(gameState)
            # finalEval += self.kingConnection(gameState)
            finalEval += self.kingCenter(gameState)
            finalEval += self.kingEncroachment(gameState)
            finalEval += self.kingOpposition(gameState, finalEval)
        return finalEval
        return 5
    
    def kingOpposition(self, gameState, eval):
        if gameState.getColor() == "W":
            wK = gameState.ownKing
            bK = gameState.opponentKing
        else:
            bK = gameState.ownKing
            wK = gameState.opponentKing

        dist = getKingDistance(bK.getCoords(), wK.getCoords())
        if dist <= 3.5:
            if eval > 0:
                return self.oppositionFactor/dist
            else:
                return (-1*self.oppositionFactor)/dist
        return 0


    def kingEncroachment(self, gameState):  
        whiteKE = self.getEncroachment(gameState, "W")
        blackKE = self.getEncroachment(gameState, "B")
        dif = whiteKE - blackKE
        if dif == 0:
            return 0
        return self.encroachmentFactor/dif


    def getEncroachment(self, gameState, color):
        
        if gameState.getColor() == color:
            sum = 0
            kingCoords = gameState.opponentKing.getCoords()
            pieces = gameState.friendPieces
            for piece in pieces:
                pieceType = piece.getType()
                level = self.encroachmentLevels[pieceType]
                if level != 0:
                    coords = piece.getCoords()
                    sum += level * getRealDistance(kingCoords, coords)
        else:
            sum = 0
            kingCoords = gameState.ownKing.getCoords()
            pieces = gameState.enemyPieces
            for piece in pieces:
                pieceType = piece.getType()
                level = self.encroachmentLevels[pieceType]
                if level != 0:
                    coords = piece.getCoords()
                    sum += level * getRealDistance(kingCoords, coords)
        return sum


    def kingCenterIndividual(self, king):
        coords = king.coords
        distanceFromEdge = 5 - getKingDistance((3.5, 3.5), coords)
        return math.log(distanceFromEdge + 1)

    def kingCenter(self, gameState):
        blackCenter = self.kingCenterIndividual(gameState.blackKing)
        whiteCenter = self.kingCenterIndividual(gameState.whiteKing)
        connectionEval = (whiteCenter - blackCenter)*self.kingCenterFactor
        return connectionEval

    def mates(self, mate):
        if mate == "Checkmate":
            return "CM"
        if mate == "Stalemate":
            return "SM"
        
    def evaluateMaterial(self, gameState):
        whiteMaterial, blackMaterial = gameState.getMaterial()
        materialDifference = whiteMaterial - blackMaterial
        eval = materialDifference
        return eval
        
        # if self.validLog(whiteMaterial, blackMaterial):
        #     base = self.materialBase
        #     logMultiplier = self.materialLogMultiplier
        #     ratioBonus = logMultiplier * math.log(whiteMaterial/blackMaterial, base)
        #     eval = materialDifference + ratioBonus
        # else:
        #     eval = materialDifference
        # return eval
    

    def validLog(self, m1, m2):
        if m1-m2 != 0 and m1 != 0 and m2 != 0:
            return True
        else:
            return False   

    def getDevelopment(self, gameState):
        team1 = self.evaluateDevelopment(gameState)
        team2 = self.evaluateDevelopment(gameState.makeFlip())
        if gameState.getColor() == "W":
            white = team1
            black = team2
        else:
            black = team1
            white = team2
        return self.devFactor * (white - black)

    def kingConnection(self, gameState):
        blackConnection = self.kingProximityValue(gameState.blackKing, gameState.blackPieces)
        
        whiteConnection = self.kingProximityValue(gameState.whiteKing, gameState.whitePieces)
        connectionEval = (whiteConnection - blackConnection)*self.kingConnectionFactor
        return connectionEval

    def kingProximityValue(self, king, pieces):
        averageValue = 0
        kingCoords = king.getCoords()
        if len(pieces) > 1:
            totalValue = 0
            for piece in pieces:
                if piece.getType() != "K":
                    pieceCoords = piece.getCoords()
                    distance = getRealDistance(pieceCoords, kingCoords)
                    totalValue += 8/distance**2
            averageValue = totalValue/(len(pieces)-1)
        if king.hasMoved:
            averageValue -= 1
        return averageValue
        
    def evaluateDevelopment(self, gameState):
        total = 0
        developmentDict = {"N" : 3, "B" : 2.9, "R" : 2, "Q": 0.2,}
        pieces = gameState.friendPieces
        for piece in pieces:
            if piece.getType() in developmentDict:
                value = developmentDict[piece.getType()] * len(piece.getPossibleMoves())
                total += value
        return total

    def pawnEvaluate(self, gameState):
        whiteEval = self.individualPawnEval(gameState, 'W')
        blackEval = self.individualPawnEval(gameState, 'B')
        return self.pawnFactor * (whiteEval - blackEval)
        
    def individualPawnEval(self, gameState, color):
        #could save time with new gA func
        eval = 0
        if gameState.getColor() == color:
            for pawn in gameState.friendPawns:
                eval += pawn.getAdvancement()
        else:
            for pawn in gameState.enemyPawns:
                eval += (7-pawn.getAdvancement())
        return eval
        
def getKingDistance(coords1, coords2):
    deltaX = abs(coords1[0] - coords2[0])
    deltaY = abs(coords1[1] - coords2[1])
    # return deltaX + deltaY
    return max(deltaX, deltaY)

def getRealDistance(coords1, coords2):
    deltaX = abs(coords1[0] - coords2[0])
    deltaY = abs(coords1[1] - coords2[1])
    distance = math.sqrt(deltaX**2 + deltaY**2)
    return distance

