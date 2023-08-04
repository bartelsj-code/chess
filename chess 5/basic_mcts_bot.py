from bot import Bot
from math import inf, sqrt, log
from gamestate_pieces import *
from random import shuffle, randint
from gui import GUI

from time import perf_counter, sleep

###############################  MCTS  Bot  #################################

class BasicMCTSBot(Bot):
    def __init__(self, color, board, searches, ef):
        super().__init__(color, board)
        # self.gui1 = GUI("rollout_start", 400, "W", 0.01)
        # self.gui2 = GUI("rollout", 400, "W", 0.3)
        self.searches = searches
        self.exploration_factor = ef
        self.evaluator = HeuristicEvaluator()

    def choose_move(self):
        gamestate = self.board.position.perfect_clone()
        root = MCTSnode(gamestate, None)
        move = self.mcts(root)
        return move

    def mcts(self, root):
        self.root = root
        best_move = None
        for i in range(self.searches):
            # print(i/self.searches)
            self.i = i
            # print(self.root.children)
            # print(searches_completed/self.searches)
            node = self.traverse_tree(root)
            if not node.is_terminal():
                node = self.expansion(node)
            value = self.rollout(node)
            self.backpropagate(node, value)
        max_value = -inf   
        for child in root.children:
            value = child.total_score/child.number_of_visits
            if value > max_value:
                max_value = value
                best_move = child.gamestate.previous_move
        return best_move

    def traverse_tree(self, node):
        while node.is_leaf == False:
            node = self.get_best_child(node)
        return node
    
    def get_best_child(self, node):
        children = node.get_children()
        best_child = select_random(children)
        for child in children:
            secure_component = child.total_score/(child.number_of_visits + 1)
            try:
                exploration_component = sqrt(log(self.i)/child.number_of_visits)
            except:
                exploration_component = inf
            child.ucb_value = secure_component + self.exploration_factor * exploration_component
        best_value = -inf
        best_child = None
        for child in children:
            if child.ucb_value > best_value:
                best_value = child.ucb_value
                best_child = child
        return best_child

    def expansion(self, node):
        if node.number_of_visits == 0:
            return node
        else:
            node.make_children()
            node.is_leaf = False
            return node.get_children()[0]
        
    def rollout(self, node):
        gamestate = node.gamestate
        # self.gui1.transition_to_gamestate(self.root.gamestate)
        # self.gui1.transition_to_gamestate(gamestate)
        for i in range(10):
            # self.gui2.transition_to_gamestate(gamestate)
            result = gamestate.check_if_terminal()
            if result != None:
                if result == "Stalemate":
                    return 0
                if gamestate.active_player == self.color:
                    return -100
                else:
                    return 100
            moves = gamestate.get_possible_moves()
            move = select_random(moves)
            gamestate = gamestate.clone_with_move(move)
        return 0
    
    def backpropagate(self, node, value):
        while node != None:
            node.total_score += value
            node.number_of_visits += 1
            node = node.parent


class MCTSnode:
    def __init__(self, gamestate, parent):
        self.total_score = 0
        self.number_of_visits = 0
        self.parent = parent
        self.gamestate = gamestate
        self.is_leaf = True
        self.children = []

    def is_terminal(self):
        if self.gamestate.check_if_terminal() != None:
            return True
        return False

    def get_children(self):
        return self.children
    
    def make_children(self):
        moves = self.gamestate.get_possible_moves()
        for move in moves:
            child_gs = self.gamestate.clone_with_move(move)
            child_node = MCTSnode(child_gs, self)
            self.children.append(child_node)
    
    def __repr__(self):
        return str(int(self.total_score/(self.number_of_visits+1))) + ","+str(self.number_of_visits)


def select_random(lst):
    return lst[randint(0, len(lst)-1)]


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