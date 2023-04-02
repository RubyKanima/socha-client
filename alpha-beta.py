import random
import logging
import collections
compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
from socha import *

class Logic(IClientHandler):
    game_state: GameState

    def move_hash(self, state: GameState):
        move_list = []
        for move in state.first_team.moves:
            move_str = str(move.to_value.x)+str(move.to_value.y)+str(move.team_enum.name)
            move_list.append(move_str)
        for move in state.second_team.moves:
            move_str = str(move.to_value.x)+str(move.to_value.y)+str(move.team_enum.name)
            move_list.append(move_str)
        return str(set(move_list))

    def min_max(self, new_state: GameState, depth: int, alpha, beta, memo : dict = {}, end : bool = False) -> list[int,dict] :
            hash_list = self.move_hash(new_state)
            value = self.evaluate(new_state)
            if hash_list in memo:
                #logging.info("!!!!!!!!!!!!!!!!!!!!!!")
                if end:
                    return [memo[hash_list], memo]
                return memo[hash_list]
            #logging.info(str(self.move_hash(new_state)))
            if depth == 0 or new_state.current_team == None:
                return value #  value berechnen
            maximizing = (new_state.current_team.name == self.game_state.current_team.name)
            
            #logging.info("Maximizing: "+ str(maximizing) +";  "+ str(new_state.current_team.name) +"|"+ str(self.game_state.current_team.name))#,"| Teams :", new_state.current_team, self.game_state.current_team)
            #logging.info("Possible: "+ str(new_state.possible_moves))
            #logging.info("Move-To: " + str(move.to_value))
            #logging.info(str(new_state.board.pretty_print()))
            if maximizing:
                if new_state.possible_moves == []:
                    if end:
                        return [value, memo]
                    return value
                maxEval = -100 # replacement (- inf)
                for child in new_state.possible_moves:
                    eval = self.min_max(new_state.perform_move(child), depth - 1, alpha, beta, memo, False)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                memo[hash_list] = maxEval
                if end:
                    return [maxEval, memo]
                else:
                    return maxEval
            
            else:
                minEval = 100 # replacement (- inf)
                for child in new_state.possible_moves:
                    eval = self.min_max(new_state.perform_move(child), depth - 1, alpha, beta, memo , False)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                memo[hash_list] = minEval
                if end:
                    return [minEval, memo]
                else:
                    return minEval
    
    def evaluate(self, state: GameState) -> int:
        if (self.game_state.current_team.name == self.game_state.first_team.name):
            max = state.first_team.fish
            min = state.second_team.fish
        else:
            min = state.first_team.fish
            max = state.second_team.fish
        return max - min
    
    def max_move(self):
        max_move = None
        max_val = -1000
        # actual min_max:
        xmemo : dict = {}
        for child in self.game_state.possible_moves:
            if len(self.game_state.board.get_empty_fields()) > 48:
                mini_max = self.min_max(self.game_state.perform_move(child), 6, max_val, 100, xmemo, True)
            elif len(self.game_state.board.get_empty_fields()) > 39:
                mini_max = self.min_max(self.game_state.perform_move(child), 3, max_val, 100, xmemo, True)
            elif len(self.game_state.board.get_empty_fields()) > 33:
                mini_max = self.min_max(self.game_state.perform_move(child), 2, max_val, 100, xmemo, True)
            else:
                mini_max = self.min_max(self.game_state.perform_move(child), 1, max_val, 100, xmemo, True)
            val = mini_max[0]
            xmemo.update(mini_max[1])
            if val > max_val:
                max_move = child
                max_val = val
        '''child = self.game_state.possible_moves[random.randint(0, len(self.game_state.possible_moves)-1)]
        val = self.min_max(self.game_state, 2, max_val, 100, {})
        #logging.info(val, child)
        if val > max_val:
            max_move = child
            max_val = val'''
        return max_move
    
    def calculate_move(self) -> Move:

        if len(self.game_state.possible_moves) == 1:
            return self.game_state.possible_moves[0]
        if self.game_state.turn < 8:
            return self.game_state.possible_moves[random.randint(0, len(self.game_state.possible_moves)-1)]
        else:
            return self.max_move()
    
    def on_update(self, state: GameState):
        self.game_state = state
    
if __name__ == "__main__":
    Starter(logic = Logic())