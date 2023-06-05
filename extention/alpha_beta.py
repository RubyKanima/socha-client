from socha import *

from logic import Logic
from .intersections import *
from .board_extentions import *
class AlphaBeta():
    
    def get_alpha_beta_cut_move(logic: Logic):
        max_val = -1000
        max_move: Move = logic.game_state.possible_moves[0]
        # if turn <= 8 deleted
        move_list = Intersection.get_first_intersections(logic.game_state, logic.game_state.other_team)
        move_list = Intersection.add_missing_direction_moves(logic.game_state, move_list, logic.game_state.current_team)
        del_list = remove_solo_fields(logic.game_state, move_list)
        if not del_list == []:
            move_list = del_list
        #addition_turn = 1 if logic.game_state.turn > 8 else 0
        length = len(move_list)
        addition_len = 1 if length <= 12 else 2 if length <= 2 else 0
        #logging.info(f"addition: {addition_len}, {addition_turn}")
        
        #print_moves_board_custom(logic.game_state.board, move_list, " ", "-", "B", "E")
        #own_pretty_print_custom(logic.game_state.board, " ", "O", "T")
        logging.info(addition_len)
        for each in move_list:
            mini_max = AlphaBeta.alpha_beta_cut(logic, logic.game_state.perform_move(each), 1 + addition_len, max_val, 100)
            val = mini_max
            if val > max_val:
                max_move = each
                max_val = val
        return max_move

    def get_most_possible_move(logic: Logic):
        filter = neighbor_filter(logic.game_state.board, logic.game_state.possible_moves)
        if not filter:
            filter = logic.game_state.possible_moves
        max_val = -1
        max_move = logic.game_state.possible_moves[0]
        for move in logic.game_state.possible_moves:
            state = logic.game_state.perform_move(move)
            val = len(state.board.possible_moves_from(move.to_value))
            if val >= max_val:
                max_val = val
                max_move = move
        return max_move
    
    def get_most_possible_fish_move(logic: Logic):
        max_val = -1
        max_move = logic.game_state.possible_moves[0]

        for move in logic.game_state.possible_moves:
            state = logic.game_state.perform_move(move)
            val = get_possible_fish(state, logic.game_state.current_team.name)
            if val >= max_val:
                max_val = val
                max_move = move
        return max_move
    
    def get_least_neighbor_move(logic: Logic):
        min_val = 10
        max_move = logic.game_state.possible_moves[0]

        for move in logic.game_state.possible_moves:
            valid_n = []
            for each in move.to_value.get_neighbors(): 
                if logic.game_state.board._is_destination_valid(each):
                    valid_n.append(each)
            val = len(valid_n)
            if val <= min_val and not val == 0:
                min_val = val
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
        hash_list = AlphaBeta.move_hash(state)
        value = AlphaBeta.evaluate_fish(logic, state)

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
                eval = AlphaBeta.alpha_beta_fish(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            memo[hash_list] = maxEval
            return maxEval

        else:
            minEval = 100 # replacement ( inf)
            for child in state.possible_moves:
                eval = AlphaBeta.alpha_beta_fish(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
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

        hash_list = AlphaBeta.move_hash(state)
        value = Intersection.delta_possibles(logic, state)
        if depth == 0 or state.current_team == None:
            return value
        move_list = Intersection.get_first_intersections(state, state.other_team)
        move_list = Intersection.add_missing_direction_moves(state, move_list, state.current_team)
        del_list = remove_solo_fields(state, move_list)
        if not del_list == []:
            move_list = del_list

        if hash_list in memo:
            return memo[hash_list]
        
        maximizing = (state.current_team.name == logic.game_state.current_team.name)
        if maximizing:
            if state.possible_moves == []:
                return value
            
            maxEval = -100 # replacement (- inf)
            for child in move_list:
                eval = AlphaBeta.alpha_beta_cut(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            memo[hash_list] = maxEval
            return maxEval

        else:
            minEval = 100 # replacement ( inf)
            for child in move_list:
                eval = AlphaBeta.alpha_beta_cut(logic, state.perform_move(child), depth - 1, alpha, beta, memo)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            memo[hash_list] = minEval
            return minEval    
    


    def get_tri_alpha_move(logic: Logic,):
        max_val = -1000
        max_move: Move = logic.game_state.possible_moves[0]
        # if turn <= 8 deleted
        #move_list = get_possible_moves_from_team(logic.game_state.board, logic.game_state.current_team.name)
        move_list = logic.game_state.possible_moves
        """
        other_moves = get_possible_moves_from_team(logic.game_state.board, logic.game_state.current_team.opponent.name)
        move_list: list[Move] = Joins.left_inner_join_on(own_moves, other_moves, "to_value", False)
        move_list = Intersection.add_missing_direction_moves_board(logic.game_state.board, move_list, logic.game_state.current_team)
        """
        """
        print("TriEval")
        print(AlphaBeta.tri_eval(logic.tri_board, logic.game_state.current_team))

        if logic.game_state.current_team.name.name == "ONE":
            print_moves_board_custom(logic.game_state.board, move_list," ", "-", "⛇", "ඞ")
        else:
            print_moves_board_custom(logic.game_state.board, move_list," ", "-", "ඞ", "⛇")
        """
        for each in move_list:
            mini_max = AlphaBeta.tri_alpha(logic.tri_board.perform_move(each), logic.game_state.current_team, 0 , logic.tri_board.board.get_field(each.to_value).fish, False, max_val, 1000)
            val = mini_max
            if val > max_val:
                max_move = each
                max_val = val
        return max_move

    
    def tri_alpha(tri_board: TriBoard, global_team: Team, depth: int, fish: int, maximizing:bool, alpha: int, beta:int):
        ''''''
        """
        print_common(tri_board.board, "ONE")
        print(f"current team: {tri_board.current_team.name.name} | {maximizing}")
        """
        """
        own_moves = get_possible_moves_from_team(tri_board.board, tri_board.current_team.name)
        other_moves = get_possible_moves_from_team(tri_board.board, tri_board.current_team.opponent.name)

        if not tri_board.is_any_contest() or depth == 0 or not own_moves or other_moves:
            if maximizing:
                return AlphaBeta.tri_eval(tri_board, global_team) - fish
            else:
                return AlphaBeta.tri_eval(tri_board, global_team) + fish

        move_list: list[Move] = Joins.left_inner_join_on(own_moves, other_moves, "to_value", False)
        move_list = Intersection.add_missing_direction_moves_board(tri_board.board, move_list, tri_board.current_team)
        if not move_list:
            move_list = own_moves
        """
        move_list = get_possible_moves_from_team(tri_board.board, tri_board.current_team.name)

        if not tri_board.is_any_contest() or depth == 0 or not move_list:
            return AlphaBeta.tri_eval2(tri_board, global_team) + fish

        if maximizing:
            maxEval = -1000
            for move in move_list:
                updated_board = tri_board.perform_move(move)
                eval = AlphaBeta.tri_alpha(updated_board, global_team, depth-1, fish + tri_board.board.get_field(move.to_value).fish, False, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(eval, alpha)
                if beta <= alpha:
                    break
            return maxEval
                
        else:
            minEval = 1000
            for move in move_list:
                updated_board = tri_board.perform_move(move)
                eval = AlphaBeta.tri_alpha(updated_board, global_team, depth-1, fish - tri_board.board.get_field(move.to_value).fish, True, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval
        
    def tri_eval(tri_board: TriBoard, global_team: Team):
        '''all subgroups'''
        global_subgroups : list[Subgroup] = []
        for group in tri_board.groups:
            #print_group_board_color(tri_board.board, group, "ONE") 
            for subgroups in group.subgroups:
                global_subgroups.append(subgroups)
        ''''''
        value = 0

        '''
        for penguin in tri_board.board.get_teams_penguins(global_team.name):
            penguin_subgroups = global_subgroups.copy()
            for direction in Vector().directions:
                for i in range(1,8):
                    destination = penguin.coordinate.add_vector(direction.scalar_product(i))
                    if not own_is_destination_valid(tri_board.board ,destination):
                        break
                    value += tri_board.board.get_field(destination).fish
                    """
                    this_hash = own_hash(destination)
                    for subgroup in penguin_subgroups:
                        if this_hash in subgroup.group:
                            value += subgroup.fish  
                            penguin_subgroups.remove(subgroup)"""

        for penguin in tri_board.board.get_teams_penguins(global_team.opponent.name):
            penguin_subgroups = global_subgroups.copy()
            for direction in Vector().directions:
                for i in range(1,8):
                    destination = penguin.coordinate.add_vector(direction.scalar_product(i))
                    if not own_is_destination_valid(tri_board.board ,destination):
                        break
                    value -= tri_board.board.get_field(destination).fish
                    """
                    this_hash = own_hash(destination)
                    for subgroup in penguin_subgroups:
                        if this_hash in subgroup.group:
                            value -= subgroup.fish
                            penguin_subgroups.remove(subgroup)"""
                    '''
        value += get_possible_fish_board(tri_board.board, global_team.name)
        value -= get_possible_fish_board(tri_board.board, global_team.opponent.name)
        
        for this_group in tri_board.groups:
            if this_group.contains_team(global_team.name.name):
                value += this_group.fish
            if this_group.contains_team(global_team.opponent.name.name):
                value -= this_group.fish

        return value
    
    def tri_eval2(tri_board: TriBoard, global_team: Team):
        check_list = {}
        for group in tri_board.groups:
            for key in group.group:
                check_list[key] = group.group[key].fish

        own_coords = [each.coordinate for each in tri_board.board.get_teams_penguins(global_team.name)]
        other_coords = [each.coordinate for each in tri_board.board.get_teams_penguins(global_team.opponent.name)]
        #print(other_coords)
        own_value = get_depth_possibles(tri_board.board, check_list.copy(), own_coords)
        other_value = get_depth_possibles(tri_board.board, check_list.copy(), other_coords)
        #print(own_value, other_value)
        #value = 0
        #for group in tri_board.groups:
        #    if group.is_contesting() or group.penguins == []:
        #        continue
        #    if group.penguins[0].team_enum.name == global_team.name.name:
        #        value += group.fish
        #    else:
        #        value -= group.fish

        return own_value - other_value# + value
    
    def tri_eval_print(tri_board: TriBoard, global_team: Team):
        check_list = {}
        for group in tri_board.groups:
            if group.is_contesting():
                for key in group.group:
                    check_list[key] = group.group[key].fish

        own_coords = [each.coordinate for each in tri_board.board.get_teams_penguins(global_team.name)]
        other_coords = [each.coordinate for each in tri_board.board.get_teams_penguins(global_team.opponent.name)]
        #print(other_coords)
        own_value = get_depth_possibles(tri_board.board, check_list.copy(), own_coords)
        other_value = get_depth_possibles(tri_board.board, check_list.copy(), other_coords)

        own_value2 = 0
        other_value2 = 0
        for group in tri_board.groups:
            if group.is_contesting() or group.penguins == []:
                continue
            if group.penguins[0].team_enum.name == global_team.name.name:
                own_value2 += group.fish
            else:
                other_value2 -= group.fish
        

        print(own_value, -other_value, own_value2, other_value2)