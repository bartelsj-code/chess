from bot import Bot
from math import inf
from gamestate_pieces import *
from random import shuffle

##################################  Minimax  Bot  #################################

class BasicMinimaxBot(Bot):
    def __init__(self, color, board, depth):
        super().__init__(color, board)
        self.depth = depth
        self.evaluator = HeuristicEvaluator()

    def choose_move(self):
        gamestate = self.board.position.perfect_clone()
        move = self.minimax_executor(gamestate)
        return move

    def minimax_executor(self, gamestate):
        moves = gamestate.get_possible_moves()
        shuffle(moves)
        for move in moves:
            child = gamestate.clone_with_move(move)
            move.value = self.minimax(child, self.depth)
        if self.color == "W":
            moves.sort(key = lambda move: move.value, reverse=True)
        else:
            moves.sort(key = lambda move: move.value, reverse=False)
        return moves[0]
        
    def minimax(self, gamestate, depth):
        result = gamestate.check_if_terminal()
        if result != None:
            if result == "Stalemate":
                return 0
            else:
                if gamestate.active_player == "W":
                    return -inf
                else:
                    return inf
        if depth == 0:
            return self.evaluator.evaluate(gamestate)
        moves = gamestate.get_possible_moves()
        if gamestate.active_player == "W":
            value = -inf
            for move in moves:
                child = gamestate.clone_with_move(move)
                value = max(self.minimax(child, depth-1), value)
            return value
        else:
            value = inf
            for move in moves:
                child = gamestate.clone_with_move(move)
                value = min(self.minimax(child, depth-1), value)
            return value
            
    def do_turn(self):
        return super().do_turn()
    
#####################################  Heuristic Evaluator  ############################

species_values = {GamestatePawn: 1, GamestateKnight: 3, GamestateBishop: 3, GamestateRook: 5, GamestateQueen: 9, GamestateKing:0}

class HeuristicEvaluator:
    def __init__(self) -> None:
        pass

    def evaluate(self, gamestate):
        white_sum = self.get_value_sum("W", gamestate)
        black_sum = self.get_value_sum("B", gamestate)
        total = white_sum-black_sum
        return total
    
    def get_value_sum(self, color, gamestate):
        value = 0
        for piece in gamestate.piece_collections[color]:
            value += species_values[type(piece)]
        return value

