from socha import *
from logic import Logic

class Tree():

    def get_depth_move(logic: Logic) -> Move:
        '''
        returns a `Move` which leads to the most accessable Fields as possible
        '''
        max_move: Move
        max_val: int = 0
        for each in logic.game_state.possible_moves:
            val = Tree.depth(logic, logic.game_state.perform_move(each), 1)
            if val < max_val:
                max_val = val
                max_move = each
        return max_move
    
    def _get_depth_move(logic: Logic) -> Move:
        '''
        returns a `Move` which leads to the most accessable Fields as possible
        only use when the other team has no possible moves left!
        '''
        max_move: Move
        max_val: int = 0
        for each in logic.game_state.possible_moves:
            val = Tree._depth(logic.game_state.perform_move(each), 0)
            if val > max_val:
                max_val = val
                max_move = each
        return max_move
    
    def _depth(state: GameState, this_val = 0, alpha = 0):
        if state.current_team == None:
            return 0
        
        max_val = 0

        for each in state.possible_moves:
            this_val = Tree._depth(state.perform_move(each), this_val + 1, alpha)
            if alpha > this_val:
                break
            alpha = this_val
        return max(max_val, this_val)
    
    def _depth_moves(state: GameState, all_move_sets = []):
        if state.current_team == None:
            all_fields = state.board.get_all_fields()
            not_zeros = [each for each in all_fields if each.fish > 0]
            return len(not_zeros)
        min_val = 100
        for each in state.possible_moves:
            val = Tree._depth(state.perform_move(each))
            min_val = min(min_val, val)
        return min_val

    def depth(logic: Logic, state: GameState):
        '''
        `depth_search()` is a recursive function to calculate the highest depth value of all possible moves.

        This one is the save version of the depth search and can always be used.
        '''
        if state.current_team == None:
            return 1
        # 1st exception if the game ended
        maximizing = (state.current_team.name == logic.game_state.current_team.name)
        if maximizing:
            max_val = 0
            if state.possible_moves == []:
                    return 1
        # 2nd exception if the own team has no possible moves
            for each in state.possible_moves:
                val = Tree.depth(logic, state.perform_move(each))
                max_val = max(max_val,val)
            return max_val + 1
        # 3rd exception if current team has possible moves
        else:
            min_val = 100
            for each in state.possible_moves:
                val = Tree.depth(logic, state.perform_move(each))
                max_val = max(max_val,val)
            return max_val - 1
        #4th exception if the other team has possible moves