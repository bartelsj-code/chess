from player import Player
import random
from gameState import GameState
from evaluator2 import Evaluator
from time import perf_counter
import math
from gameStateEmpty import GameStateEmpty
from gameStateHolder import GameStateHolder

class Engine(Player):
    def __init__(self, color, board, evaluationCap):
        super().__init__(color, board)
        # random.seed(3)
        self.evaluator = Evaluator()
        self.evaluationCap = evaluationCap
        self.depthCap = 15
        self.currentCount = 0
        self.oldCheck = 0
        
    def doTurn(self, lastmove):
        self.evaluator.moves_made += 1
        self.currentCount = 0
        self.quitting = False
        startTime = perf_counter()
        startingGS = self.getGameStateFromBoard()
        gsHolder = GameStateHolder(startingGS, None)
        for haltDepth in range(1, self.depthCap):

      
            self.terminateCheck()
            
            self.evalDict = {}
            alpha, beta = 0 - 10**100, 10**100

            eval = self.minimax(gsHolder, alpha, beta, 0, haltDepth)
            if eval >= 1000 or eval <= -1000:
                self.quitting = True
            if self.quitting:
                break
            print("ranking: {}, {}/{}, depth: {}".format(gsHolder.evaluatedChildren, self.currentCount, self.evaluationCap, haltDepth))
   
        
   
        bestMove = gsHolder.evaluatedChildren[0].priorMove
        endTime = perf_counter()
        self.doMoveSequence(bestMove)
       
        thoughtTime = endTime - startTime
        print("processing time: {}".format(thoughtTime))
        return bestMove
    
    def terminateCheck(self):
        if self.evaluationCap-self.currentCount<self.currentCount - self.oldCheck:
            self.quitting = True
        self.oldCheck = self.currentCount
        
        
    def minimax(self, gameStateHolder, alpha, beta, depth, haltDepth):
        if self.currentCount > self.evaluationCap:
            self.quitting = True

        if self.quitting:
            return 0
        id = gameStateHolder.gameState.toString() + str(depth)
        if id in self.evalDict and depth >= 1:
            return self.evalDict[id]
        mateEval = self.evaluator.mateOnlyEvaluate(gameStateHolder.gameState)
        if mateEval == "CM":
            if self.isMaximizing(gameStateHolder.gameState):
                eval = -100000000 / (depth + 1)
                gameStateHolder.eval = eval
            else:
                eval = 100000000 / (depth + 1)
                gameStateHolder.eval = eval
            return eval
        if mateEval == "SM":
            gameStateHolder.eval = 0
            return 0

        if depth >= haltDepth:
            eval = self.evaluator.evaluate(gameStateHolder.gameState)
            self.currentCount += 1
            gameStateHolder.eval = eval
            self.evalDict[id] = eval
            return eval
        
        if not gameStateHolder.movesGenerated:
            gameStateHolder.generateMoves()
            if depth == 0:
                random.shuffle(gameStateHolder.unevaluatedMoves)
            # self.sortMoves(gameStateHolder.unevaluatedMoves)

        if self.isMaximizing(gameStateHolder):
            pruned = False
            maxEval = -1*(10**60)
            for child in gameStateHolder.evaluatedChildren:
                eval = self.minimax(child, alpha, beta, depth+1, haltDepth)
                if self.quitting:
                    return 0
                if eval > maxEval:
                    maxEval = eval
                    alpha = eval
                if self.shouldPruneRemainingMoves(alpha, beta):
                    pruned = True
                    break

            while len(gameStateHolder.unevaluatedMoves) > 0 and not pruned:
                move = gameStateHolder.unevaluatedMoves.pop()
                oppositeView = gameStateHolder.gameState.flipWithMove(move)
                oppositeViewHolder = GameStateHolder(oppositeView, move)
                gameStateHolder.evaluatedChildren.append(oppositeViewHolder)
                eval = self.minimax(oppositeViewHolder, alpha, beta, depth+1, haltDepth)
                if self.quitting:
                    return 0
                if eval > maxEval:
                    maxEval = eval
                    alpha = eval
                if self.shouldPruneRemainingMoves(alpha, beta):
                    break

            self.evalDict[id] = maxEval
            gameStateHolder.sortChildren()
            gameStateHolder.eval = maxEval
            return maxEval
        else:
            pruned = False
            minEval = 10**60
            for child in gameStateHolder.evaluatedChildren:
                eval = self.minimax(child, alpha, beta, depth+1, haltDepth)
                if self.quitting:
                    return 0
                if eval < minEval:
                    minEval = eval
                    beta = minEval
                if self.shouldPruneRemainingMoves(alpha, beta):
                    pruned = True
                    break
            
            while len(gameStateHolder.unevaluatedMoves) > 0 and not pruned:
                move = gameStateHolder.unevaluatedMoves.pop()
                oppositeView = gameStateHolder.gameState.flipWithMove(move)
                oppositeViewHolder = GameStateHolder(oppositeView, move)
                gameStateHolder.evaluatedChildren.append(oppositeViewHolder)
                eval = self.minimax(oppositeViewHolder, alpha, beta, depth+1, haltDepth)
                if self.quitting:
                    return 0
                if eval < minEval:
                    minEval = eval
                    beta = minEval
                if self.shouldPruneRemainingMoves(alpha, beta):
                    break

            self.evalDict[id] = minEval
            gameStateHolder.sortChildren()
            gameStateHolder.eval = minEval
            return minEval


        
    # def captures(self, move):
    #     if move.isCap:
    #         ownValue = move.piece.getValue()
    #         takenValue = move.captureValue
    #         difference = takenValue / ownValue
    #         return difference
    #     else:
    #         return 0

    # def type(self, move):
    #     bonusDict = {"N": 4, "B" : 4, "P": 4, "K": 1.1, "R": 1 , "Q": 0}
    #     return bonusDict[move.piece.getType()]

    # def center(self, move):
    #     if move.piece.getType() in {"P","N"}:
    #         return 6 - self.getDistanceFromMiddle((move.newX, move.newY))
    #     return 0

    # def getDistanceFromMiddle(self, coords):
    #     deltaX = abs(3.5-coords[0])
    #     deltaY = abs(3.5-coords[1])
    #     return max(deltaX, deltaY)

    # def sortMoves(self, moves):
    #     # random.shuffle(moves)
    #     capMultiplier = 20
    #     typeMultiplier = 2
    #     centerMultiplier = 1
    #     for move in moves:
    #         move.evaluation = 0
    #         move.evaluation += capMultiplier * self.captures(move)
    #         move.evaluation += typeMultiplier * self.type(move)
    #         move.evaluation += centerMultiplier * self.center(move)
    #     moves.sort(key=lambda x: x.evaluation)
     
    def isMaximizing(self, gs):
        if gs.color == 'W':
            return True
        else:
            return False
    
    def shouldPruneRemainingMoves(self, alpha, beta):
        # return False
        return alpha >= beta
