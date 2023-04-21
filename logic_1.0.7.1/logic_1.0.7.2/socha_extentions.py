from socha import *
from joins import *
from logic import Logic
from typing import List, Union, Optional
from socha_extentions import *

class Tile(Field):

    def __init__(self):
        self.neighbors = self.coordinate.get_neighbors()

    def _expand(_tile) -> list:
        list = []
        for each in _tile.neighbors:
            if each not in list:
                list.append(Tile._expand(_tile, list))
        return list.append(_tile)


    def is_valuable(_tile) -> bool:
        return _tile.fish in [2,3,4]

class CustomBoard(Board):
    def __init__(self):
        self.blobs = self._get_all_blobs(self)

    def _get_all_blobs(_board):
        '''missing code'''


    def _create_blob(_board: Board):
        '''missing code'''
            


    def del_fields(_board: Board, _del: List[int] | int) -> Board:
        if isinstance(_del, int):
            _del = [].append(_del)
        new_board: List[List[Field]] = []
        for row in _board.board:
            row_list = []
            for field in row:
                if field.fish in _del or field.penguin:
                    row_list.append(Field(HexCoordinate(field.coordinate.x, field.coordinate.y), None, 0))
                else:
                    row_list.append(field)
            new_board.append(row_list)
        return Board(new_board)

    def filter_fields(_board: Board, filter: int):
        filter_list = [0,1,2,3,4].remove(filter)
        return CustomBoard.del_fields(_board, filter_list)

class Blob():

    def __init__(self, blob: List[Field]):
        self.blob = blob
        self.fish = self._get_fish_val()
        self.quantity = len(blob)
    
    def _get_fish_val(self) -> int:
        fish = 0
        for each in self.blob:
            fish += each.fish
        return fish
    
    def _create_blob(self, _board: Board):
        new_board = CustomBoard.del_ones(_board)


class Alpha_Beta():

    def get_alpha_beta_fish_move(logic: Logic):
        max_val = -1000
        max_move: Move = logic.game_state.possible_moves[0]
        # actual alpha_beta:
        for each in logic.game_state.possible_moves:
            if len(logic.game_state.board.get_empty_fields()) > 50:
                mini_max = Alpha_Beta.alpha_beta_fish(logic, logic.game_state.perform_move(each), 2, max_val, 100)
            else:
                mini_max = Alpha_Beta.alpha_beta_fish(logic, logic.game_state.perform_move(each), 1, max_val, 100)
            val = mini_max
            if val > max_val: 
                max_move = each
                max_val = val
        return max_move
    
    def get_alpha_beta_inters_move(logic: Logic):
        max_val = -1000
        max_move: Move = logic.game_state.possible_moves[0]
        # actual alpha_beta:
        left = logic.game_state.possible_moves
        right = Logic.get_possible_movements(logic.game_state, logic.game_state.current_team.opponent)
        move_list = Joins.left_inner_join_on(left, right, "to_value") if not right == [] else left
        for each in move_list:
            mini_max = Alpha_Beta.alpha_beta_inters(logic, logic.game_state.perform_move(each), 1, max_val, 100)
            val = mini_max
            if val > max_val:
                max_move = each
                max_val = val
        return max_move
    
    def get_alpha_beta_cut_move(logic: Logic):
        max_val = -1000
        max_move: Move = logic.game_state.possible_moves[0]
        # actual alpha_beta:
        left = logic.game_state.possible_moves
        right = Logic.get_possible_movements(logic.game_state, logic.game_state.current_team.opponent)
        move_list = Joins.left_inner_join_on(left, right, "to_value") if not right == [] else left
        addition = 1 if len(move_list) < 5 else -1 if len(move_list) > 15 else 0
        logging.info(f"addition: {addition}")
        for each in move_list:
            mini_max = Alpha_Beta.alpha_beta_cut(logic, logic.game_state.perform_move(each), 1 + addition, max_val, 100)
            val = mini_max
            if val > max_val:
                max_move = each
                max_val = val
        return max_move
    
    def get_most_possible_move(logic: Logic):
        max_val = -1
        max_move: Move = logic.game_state.possible_moves[0]
        
        for move in logic.game_state.possible_moves:
            state = logic.game_state.perform_move(move)
            val = len(state.board.possible_moves_from(move.to_value))
            #logging.info(f"{val}, {state.board.possible_moves_from(move.to_value)}, {move.to_value}")
            if val > max_val:
                max_val = val
                max_move = move
        return max_move
    
    def move_hash(state: GameState):
        move_list = []
        for move in state.first_team.moves:
            move_str = str(move.to_value.x)+str(move.to_value.y)+str(move.team_enum.name)
            move_list.append(move_str)
        for move in state.second_team.moves:
            move_str = str(move.to_value.x)+str(move.to_value.y)+str(move.team_enum.name)
            move_list.append(move_str)
        return str(set(move_list))

    def evaluate_fish(logic: Logic, state: GameState) -> int:
        if (logic.game_state.current_team.name == logic.game_state.first_team.name):
            max = state.first_team.fish
            min = state.second_team.fish
        else:
            min = state.first_team.fish
            max = state.second_team.fish
        return max - min

    def alpha_beta_fish(logic: Logic, state: GameState, depth: int, alpha, beta, memo : dict = {}):
        '''
        `alpha_beta_fish()` only uses the `fish` value for the evaluation aswell as the `possible_moves`

        Arguments needed are:
            - `GameState`using the new calculated GameState
            - `depth`    defining the depth of the algorithm
            - `alpha`    for the biggest value achieved during the algorithm
            - `beta`     for the smallest value achieved during the algorithm
            - `memo`     used as a memory `dict` to remember similar paths

        '''
        hash_list = Alpha_Beta.move_hash(state)
        value = Alpha_Beta.evaluate_fish(logic, state)

        if hash_list in memo:
            return memo[hash_list]
        
        if depth == 0 or state.current_team == None:
            return value
        
        maximizing = (state.current_team.name == logic.game_state.current_team.name)
        if maximizing:
            if state.possible_moves == []:
                return value
            
            maxEval = -100 # replacement (- inf)
            for child in state.possible_moves:
                eval = Alpha_Beta.alpha_beta_fish(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            memo[hash_list] = maxEval
            return maxEval

        else:
            minEval = 100 # replacement ( inf)
            for child in state.possible_moves:
                eval = Alpha_Beta.alpha_beta_fish(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            memo[hash_list] = minEval
            return minEval

    def alpha_beta_cut(logic: Logic, state: GameState, depth: int, alpha: int, beta: int, memo: dict = {}):
        '''
        `alpha_beta_cut()` is the function for alpha beta pruning with intersections as possible_moves

        Arguments needed are:
            - `GameState`   using the new calculated GameState
            - `depth`       defining the depth of the algorithm
            - `alpha`       for the biggest value achieved during the algorithm
            - `beta`        for the smallest value achieved during the algorithm
            - `memo`        used as a memory `dict` to remember similar paths
        '''

        hash_list = Alpha_Beta.move_hash(state)
        value = Intersection.delta_possibles(logic, state)
        left = state.possible_moves
        if depth == 0 or state.current_team == None:
            return value
        
        if not state.current_team.opponent == None:
            right = Logic.get_possible_movements(state, state.current_team.opponent)
        else:
            right = []
        move_list = Joins.left_inner_join_on(left, right, "to_value") if right != [] else left
        #logging.info(f"\n left: {left} \n right: {right} \n")

        if hash_list in memo:
            return memo[hash_list]
        
        maximizing = (state.current_team.name == logic.game_state.current_team.name)
        if maximizing:
            if state.possible_moves == []:
                return value
            
            maxEval = -100 # replacement (- inf)
            for child in move_list:
                eval = Alpha_Beta.alpha_beta_cut(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            memo[hash_list] = maxEval
            return maxEval

        else:
            minEval = 100 # replacement ( inf)
            for child in move_list:
                eval = Alpha_Beta.alpha_beta_cut(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            memo[hash_list] = minEval
            return minEval    
         
    def alpha_beta_inters(logic: Logic, state: GameState, depth: int, alpha: int, beta: int, memo: dict = {}):
        '''
        `alpha_beta_cut()` is the function for alpha beta pruning with intersections as possible_moves

        Arguments needed are:
            - `GameState`   using the new calculated GameState
            - `depth`       defining the depth of the algorithm
            - `alpha`       for the biggest value achieved during the algorithm
            - `beta`        for the smallest value achieved during the algorithm
            - `memo`        used as a memory `dict` to remember similar paths
        '''

        hash_list = Alpha_Beta.move_hash(state)
        value = Alpha_Beta.evaluate_fish(logic, state)

        if depth == 0 or state.current_team == None:    #End recursion if depth == 0 or game over
            return value

        if hash_list in memo:                           #Return value if already memorized
            return memo[hash_list]
        
        left = state.possible_moves
        right = Logic.get_possible_movements(state, state.current_team.opponent)
        move_list = Joins.left_inner_join_on(left, right, "to_value") if not right == [] else left
        logging.info(f"\n left: {left} \n right: {right} \n")
        
        maximizing = (state.current_team.name == logic.game_state.current_team.name)
        if maximizing:
            if move_list == []:
                return value                            #Return value if no more possible moves
            
            maxEval = -100 # replacement (- inf)
            for child in move_list:
                eval = Alpha_Beta.alpha_beta_inters(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break                               #Break recursion if maxEval is smaller than the overall biggest eval or equal

            memo[hash_list] = maxEval
            return maxEval                              #Return biggest Number / Eval

        else:
            minEval = 100 # replacement ( inf)
            for child in move_list:
                eval = Alpha_Beta.alpha_beta_inters(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break                               #Break recursion if maxEval is smaller than the overall biggest eval or equal

            memo[hash_list] = minEval
            return minEval                              #Return smallest Number / Eval

    def alpha_beta(logic: Logic, state: GameState, depth: int, list_f = None, evaluate_f = None, alpha: int = -100, beta: int = 100, memo: dict = {}):
        '''
        `alpha_beta()` is the general function for alpha beta pruning within the min_max-algorithm

        Arguments needed are:
            - `GameState`   using the new calculated GameState
            - `depth`       defining the depth of the algorithm
            - `alpha`       for the biggest value achieved during the algorithm
            - `beta`        for the smallest value achieved during the algorithm
            - `list_f`      defining which function should be used for move_list
            - `evaluate_f`  defining which function should be used for evaluating
            - `memo`        used as a memory `dict` to remember similar paths
        '''

        hash_list = Alpha_Beta.move_hash(state)
        value = evaluate_f(state)
        move_list: list[Move] = list_f(state)

        if hash_list in memo:
            return memo[hash_list]
        
        if depth == 0 or state.current_team == None:
            return value
        
        if (state.current_team.name == logic.game_state.current_team.name):

            if state.possible_moves == []: #check if even needed because of line 107
                return value
            
            max_eval = -100
            for move in move_list:
                eval = Alpha_Beta.alpha_beta(logic, state.perform_move(move), depth-1, list_f, evaluate_f, alpha, beta, memo)
                max_eval= max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            memo[hash_list] = max_eval
            return max_eval
        
        else:

            min_eval = -100
            for move in move_list:
                eval = Alpha_Beta.alpha_beta(logic, state.perform_move(move), depth-1, list_f, evaluate_f, alpha, beta, memo)
                max_eval= min(min_eval, eval)
                alpha = min(alpha, eval)
                if beta <= alpha: break
            memo[hash_list] = min_eval
            return min_eval

                
class Intersection():

    def __init__(self, game_state, move):
        self.move: Move
        self.vector: Vector
        self.betweens: int = self._get_betweens()
        self.after: int = self._get_after()
    '''
    def get_intersection_move(logic: Logic):
        max_val = 0
        max_move: Move

        for each in logic.inters:
            val = Intersection.evaluate()'''
    
    def get_delta_cut_move(logic: Logic):
        max_val = 1000
        max_move: Move = None
        for move in logic.left_inters:
            val = Intersection.delta_possibles(logic, logic.game_state.perform_move(move))
            if val > max_val:
                max_val = val
                max_move = move
        return max_move

    def delta_possibles(logic: Logic, state: GameState) -> int: #could work with a non-quantonian function
        '''
        `delta_cut` returns the discrepancy of the current's `.possible_moves` and the opponent's `possible_moves`
        '''
        if (logic.game_state.current_team.name == logic.game_state.first_team.name):
            val = len(Logic.get_possible_movements(state, logic.game_state.first_team)) - len(Logic.get_possible_movements(state, logic.game_state.second_team))
        else:
            val = len(Logic.get_possible_movements(state, logic.game_state.second_team)) - len(Logic.get_possible_movements(state, logic.game_state.first_team))
        #logging.info(val)
        return val
    
    def delta_fish_possibles(logic:Logic, state: GameState) -> int:
        '''
        `delta_cut` returns the discrepancy of current's `fish` and the opponent's `fish`
        '''
        if (logic.game_state.current_team.name == logic.game_state.first_team.name):
            max = sum([state.board.get_field(move.to_value).fish for move in state._get_possible_moves(logic.game_state.first_team)])
            min = sum([state.board.get_field(move.to_value).fish for move in state._get_possible_moves(logic.game_state.second_team)])
        else:
            min = sum([state.board.get_field(move.to_value).fish for move in state._get_possible_moves(logic.game_state.first_team)])
            max = sum([state.board.get_field(move.to_value).fish for move in state._get_possible_moves(logic.game_state.second_team)])
        return max - min
        #test needed
        
    def _get_betweens(game_state):
        '''missing code'''

    def _get_after():
        '''missing code'''

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
            val = Tree._depth_moves(logic.game_state.perform_move(each), 1)
            if val > max_val:
                max_val = val
                max_move = each
        return max_move
    
    def _depth(state: GameState):
        if state.current_team == None:
            return 1
        
        max_val = 0
        for each in state.possible_moves:
            val = Tree._depth(state.perform_move(each))
            max_val = max(max_val, val)
        return max_val + 1
    
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

        

