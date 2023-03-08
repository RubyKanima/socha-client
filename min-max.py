import random
from socha import *

class Logic(IClientHandler):
    game_state: GameState
        
    def min_max(new_state: GameState, depth: int, maximizing: bool, new_move: Move): #
            if new_move != None:
                if depth == 0 or new_state.board.possible_moves_from(new_move.to_value) == []: 
                    return Logic.evaluate(new_state) #  value berechnen
            if maximizing:
                maxEval = -100000 # replacement (- inf)
                for child in new_state.possible_moves:
                    eval = Logic.min_max(GameState.perform_move(child), child, depth - 1, False)
                    maxEval = max(maxEval,eval)
                return maxEval
            else:
                minEval = 100000 # replacement (- inf)
                for child in new_state._get_possible_moves(new_state.other_team):
                    eval = Logic.min_max(GameState.perform_move(child), child, depth - 1, True)
                    minEval = min(minEval,eval)
                return minEval
    
    def evaluate(state: GameState):
        alpha = state.fishes.get_fish_by_team(state.current_team.team_enum)
        beta = state.fishes.get_fish_by_team(state.other_team.team_enum)
        return alpha - beta
    
    def calculate_move(self) -> Move:
        return self.min_max(self.game_state, 3, True)
    
    def on_update(self, state: GameState):
        self.game_state = state
    
if __name__ == "__main__":
    Starter(logic = Logic())