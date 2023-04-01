import random
import logging
from socha import *

class Logic(IClientHandler):
    game_state: GameState

    def min_max(self, new_state: GameState, depth: int, alpha, beta, memo = {}) -> int :
            hash_list = set(new_state.first_team.moves + new_state.second_team.moves) # Move not hashable !FIX!
            if hash_list in memo:
                return memo[hash_list]

            if depth == 0 or new_state.current_team == None:
                return self.evaluate(new_state) #  value berechnen
            maximizing = (new_state.current_team.name == self.game_state.current_team.name)
            
            #logging.info("Maximizing: "+ str(maximizing) +";  "+ str(new_state.current_team.name) +"|"+ str(self.game_state.current_team.name))#,"| Teams :", new_state.current_team, self.game_state.current_team)
            #logging.info("Possible: "+ str(new_state.possible_moves))
            #logging.info("Move-To: " + str(move.to_value))
            #logging.info(str(new_state.board.pretty_print()))
            if maximizing:
                if new_state.possible_moves == []:
                    return self.evaluate(new_state)
                maxEval = -100 # replacement (- inf)
                for child in new_state.possible_moves:
                    eval = self.min_max(new_state.perform_move(child), depth - 1, alpha, beta, child)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                memo[hash_list] = maxEval
                return maxEval
            
            else:
                minEval = 100 # replacement (- inf)
                for child in new_state.possible_moves:
                    eval = self.min_max(new_state.perform_move(child), depth - 1, alpha, beta, child)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                memo[hash_list] = minEval
                return minEval
    
    def evaluate(self, state: GameState):
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
        ''''       
        for child in self.game_state.possible_moves:
            val = self.min_max(self.game_state, 3, True, max_val, 100, child)
            print(val, child)
            if val > max_val:
                max_move = child
                max_val = val
        '''
        child = self.game_state.possible_moves[random.randint(0, len(self.game_state.possible_moves)-1)]
        val = self.min_max(self.game_state, 2, max_val, 100, child)
        #logging.info(val, child)
        if val > max_val:
            max_move = child
            max_val = val
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