from socha import *
from joins import *
from logic import Logic
from typing import List, Union, Optional
from socha_algorithms import *
from board_extentions import *
from print_extentions import *

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
    
    def get_alpha_beta_cut_move(logic: Logic):
        max_val = -1000
        max_move: Move = logic.game_state.possible_moves[0]

        # if turn <= 8 deleted
        move_list = Intersection.get_first_intersections(logic.game_state, logic.game_state.other_team)
        move_list = Intersection.add_missing_direction_moves(logic.game_state, move_list, logic.game_state.current_team)
        #addition_turn = 1 if logic.game_state.turn > 8 else 0
        addition_len = 1 if len(move_list) < 6 else 0
        #logging.info(f"addition: {addition_len}, {addition_turn}")
        
        print_moves_board_custom(logic.game_state.board, move_list, " ", "-", "O", "T")
        own_pretty_print_custom(logic.game_state.board, " ", "O", "T")
        for each in move_list:
            mini_max = Alpha_Beta.alpha_beta_cut(logic, logic.game_state.perform_move(each), 1 + addition_len, max_val, 100)
            val = mini_max
            if val > max_val:
                max_move = each
                max_val = val
        return max_move
      
    def get_alpha_beta_most_possible_move(logic: Logic):
        max_val = -1
        max_move = logic.game_state.possible_moves[0]
        turn_addition = 2 if logic.game_state.turn > 45 else 1 if logic.game_state.turn > 35 else 0

        for move in logic.game_state.possible_moves:
            val = Alpha_Beta.alpha_beta_most(logic, logic.game_state.perform_move(move), 1 + turn_addition, max_val, 100)
            if val >= max_val:
                max_val = val
                max_move = move
        return max_move
    
    def get_most_possible_move(logic: Logic):
        max_val = -1
        max_move = logic.game_state.possible_moves[0]

        for move in logic.game_state.possible_moves:
            state = logic.game_state.perform_move(move)
            val = len(state.board.possible_moves_from(move.to_value))
            if val >= max_val:
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
    
    def alpha_beta_most(logic: Logic, state: GameState, depth: int, alpha: int, beta: int, memo : dict = {}):
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
        value = len(state.possible_moves) + sum([state.board.get_field(each.to_value).fish for each in state.possible_moves])

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
                eval = Alpha_Beta.alpha_beta_most(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            memo[hash_list] = maxEval
            return maxEval

        else:
            minEval = 100 # replacement ( inf)
            for child in state.possible_moves:
                eval = Alpha_Beta.alpha_beta_most(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            memo[hash_list] = minEval
            return minEval

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
        if depth == 0 or state.current_team == None:
            return value
        move_list = Intersection.get_first_intersections(state, state.other_team)
        move_list = Intersection.add_missing_direction_moves(state, move_list, state.current_team)
        #tabulate_moves(move_list)
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
            val = len(get_possible_movements(state, logic.game_state.first_team)) - len(get_possible_movements(state, logic.game_state.second_team))
        else:
            val = len(get_possible_movements(state, logic.game_state.second_team)) - len(get_possible_movements(state, logic.game_state.first_team))
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
        
    def _get_betweens():
        '''missing code'''

    def _get_after():
        '''missing code'''

    def get_last_intersections(state: GameState, team: Team = None) -> List[Move]:
        '''only usable after 4th turn'''
        if team == None:
            team = state.current_team

        other_possible_fields = get_possible_fields(state, team.opponent)
        last_intersections = []

        for penguin in team.penguins:
            for direction in Vector().directions:
                ''' get moves in direction'''
                origin = penguin.coordinate
                final_destination = origin.add_vector(direction.scalar_product(1))

                if state.board._is_destination_valid(final_destination):
                    if state.board.get_field(final_destination).fish == 0:
                        final_destination: HexCoordinate = None
                else:
                    final_destination: HexCoordinate = None
                final_destination = None

                for i in range(1, 8):
                    destination = origin.add_vector(direction.scalar_product(i))
                    if state.board._is_destination_valid(destination):
                        destination_field = state.board.get_field(destination)
                        if destination_field in other_possible_fields:
                            final_destination = destination
                    else:
                        if final_destination:
                            last_intersections.append(Move(team.name, final_destination, origin))
                        break
        return last_intersections
    
             
    def add_missing_direction_moves(state: GameState, move_list: list[Move], team: Team = None):
        add_list = []

        if not team:
            team = state.current_team
        
        for penguin in team.penguins:
            inters_to = [each.from_value for each in move_list]
            if penguin.coordinate in inters_to:   #if the penguin has no intersection
                penguin_moves = [each for each in move_list if each.from_value == penguin.coordinate]
                penguin_missing_dir : List[Vector] = Vector().directions

                for move in penguin_moves:
                    if get_dir(move) in penguin_missing_dir:
                        penguin_missing_dir.remove(get_dir(move))

                if not penguin_missing_dir == []:
                    for direction in penguin_missing_dir:
                        destination = penguin.coordinate.add_vector(direction.scalar_product(1))
                        if state.board._is_destination_valid(destination):
                            add_list.append(Move(team.name, destination, penguin.coordinate))
            
            move_list.extend(add_list)
        return move_list

    def get_first_intersections(state: GameState, team: Team = None) -> List[Move]:
        if team == None:
            team = state.other_team
        possible_moves = state._get_possible_moves(team.opponent)

        first_intersections = []
        for penguin in team.penguins:
            for direction in Vector().directions:
                stop = False
                for i in range(1, 8):
                    if stop: break 

                    destination = penguin.coordinate.add_vector(direction.scalar_product(i))
                    if state.board._is_destination_valid(destination): # stop if end of board/ axis
                        for each in possible_moves: # add move if intersect
                            if destination == each.to_value:
                                """logging.info("!!!!!!!!!!!")
                                logging.info(str(destination)+ "  " + str(each))"""
                                first_intersections.append(each)
                                stop = True
                                break   # stop at first instance
                    else:
                        break
        #tabulate_moves(first_intersections)
        return first_intersections
           


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

        

