def minimax(self, gs, alpha, beta, depth, haltDepth):
        # id = gs.toString() + str(depth)
        # if id in self.evalDict:
        #     return self.evalDict[id]
        # eval = self.evaluator.mateOnlyEvaluate(gs)
        # if eval == "CM":
        #     if self.isMaximizing(gs):
        #         eval =  -100000000 / (depth + 1)
        #     else:
        #         eval = 100000000 / (depth + 1)
        #     return eval
        # if eval == "SM":
        #     return 0
        
        # if depth >= haltDepth:
        #     eval = self.evaluator.evaluate(gs)
        #     self.evalDict[id] = eval
        #     return eval
        # moves = gs.getAllPossibleMoves()
        # if haltDepth - depth >= 2:
        #     self.sortMoves(moves)
        if self.isMaximizing(gs):
            maxEval = -10**60
            for i in range(len(moves)):
                move = moves[i]
                if i > 0:
                    if self.shouldPruneRemainingMoves(alpha, beta):
                        break
                oppositeView = gs.flipWithMove(move)
                if depth >= haltDepth-1:
                    haltDepth += self.addDepth(gs, oppositeView, move)
                eval = self.minimax(oppositeView, alpha, beta, depth+1, haltDepth)
                if depth == 0:
                    print('(White) Move {} out of {} ({}) evaluated: {}, {}'.format(i+1,len(moves), move.toString(), eval, self.evaluator.counter))
                if maxEval < eval:
                    if depth == 0:
                        self.bestMove = move
                    maxEval = eval
                if maxEval > alpha:
                    alpha = maxEval
            self.evalDict[id] = maxEval
            return maxEval
        else:
            minEval = 10**60
            for i in range(len(moves)):
                move = moves[i]
                if i > 0:
                    if self.shouldPruneRemainingMoves(alpha, beta):
                        break
                oppositeView = gs.flipWithMove(move)
                if depth >= haltDepth -1:
                    haltDepth += self.addDepth(gs, oppositeView,move)
                eval = self.minimax(oppositeView, alpha, beta, depth+1, haltDepth)
                if depth == 0:
                    print('(Black) Move {} out of {} ({}) evaluated: {}, {}'.format(i+1,len(moves), move.toString(), eval, self.evaluator.counter))
                if minEval > eval:
                    if depth == 0:
                        self.bestMove = move
                    minEval = eval
                if minEval < beta:
                    beta = minEval
            self.evalDict[id] = minEval
            return minEval
