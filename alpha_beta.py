from socha import *
from logic import Logic
import logging


class Alpha_Beta():
    def move_hash(state: GameState):
        move_list = []
        for move in state.first_team.moves:
            move_str = str(move.to_value.x)+str(move.to_value.y)+str(move.team_enum.name)
            move_list.append(move_str)
        for move in state.second_team.moves:
            move_str = str(move.to_value.x)+str(move.to_value.y)+str(move.team_enum.name)
            move_list.append(move_str)
        return str(set(move_list))

    def evaluate(self: Logic, state: GameState) -> int:
        if (self.game_state.current_team.name == self.game_state.first_team.name):
            max = state.first_team.fish
            min = state.second_team.fish
        else:
            min = state.first_team.fish
            max = state.second_team.fish
        return max - min

    def alpha_beta_fish(self: Logic, new_state: GameState, depth: int, alpha, beta, memo : dict = {}):
        '''
        `alpha_beta_fish()` only uses the `fish` value for the evaluation aswell as the `possible_moves`
        arguments needed are:
            - `GameState`using the new calculated GameState
            - `depth`    defining the depth of the algorithm
            - `alpha`    for the biggest value achieved during the algorithm
            - `beta`     for the smallest value achieved during the algorithm
            - `memo`     used as a memory `dict` to remember similar paths

        '''
        hash_list = Alpha_Beta.move_hash(new_state)
        value = Alpha_Beta.evaluate(new_state)
        if hash_list in memo:
            return memo[hash_list]
        
        if depth == 0 or new_state.current_team == None:
            return value
        
        maximizing = (new_state.current_team.name == self.game_state.current_team.name)
        if maximizing:
            if new_state.possible_moves == []:
                return value
            
            maxEval = -100 # replacement (- inf)
            for child in new_state.possible_moves:
                eval = Alpha_Beta.alpha_beta(self, new_state.perform_move(child), depth - 1, alpha, beta, memo)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            memo[hash_list] = maxEval
            return maxEval

        else:
            minEval = 100 # replacement ( inf)
            for child in new_state.possible_moves:
                eval = Alpha_Beta.alpha_beta(self, new_state.perform_move(child), depth - 1, alpha, beta, memo)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            memo[hash_list] = minEval
            return minEval
            
    def alpha_beta(self: Logic, new_state: GameState, depth: int, alpha, beta, algorithm, memo: dict = {}):
        ''''missing code'''