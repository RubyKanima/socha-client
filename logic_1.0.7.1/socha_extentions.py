from socha import *
from logic import Logic
import logging

class Depth_Search():

    def get_depth_move(logic:Logic) -> Move:
        '''
        returns the `Move` with the most accessable `Fields` as possible
        '''
        best_move: Move = None
        best_val: int = 0
        for each in logic.game_state.possible_moves:
            val = Depth_Search._depth_search(logic, logic.game_state.perform_move(each), 1)
            if val > best_val:
                best_val = val
                best_move = each
        return best_move

    def depth_search(logic: Logic, new_state: GameState, depth: int):
        '''
        `depth_search()` is a recursive function to calculate the highest depth value of all possible moves.

        This one is the save version of the depth search and can always be used.
        '''
        if new_state.current_team == None:
            return depth
        # 1st exception if the game ended
        maximizing = (new_state.current_team.name == logic.game_state.current_team.name)
        if maximizing:
            if new_state.possible_moves == []:
                    return depth
        # 2nd exception if the own team has no possible moves
            for each in new_state.possible_moves:
                return Depth_Search.depth_search(logic, new_state.perform_move(each), depth+1)
        # 3rd exception if current team has possible moves
        else:
            for each in new_state.possible_moves:
                return Depth_Search.depth_search(logic,new_state.perform_move(each), depth)
        #4th exception if the other team has possible moves
    
    def _depth_search(logic: Logic, new_state: GameState, depth: int):
        '''
        `_depth_search()` is a recursive function to calculate the highest depth value of all possible moves.

        This should only be used if the other team has no more possible moves
        '''
        if new_state.current_team == None or new_state.possible_moves == []:
            return depth
        #1st exception if game ended
        for each in new_state.possible_moves:
                return Depth_Search._depth_search(logic, new_state.perform_move(each), depth+1)
        #2nd exception if game has not ended

class Alpha_Beta():

    def get_alpha_beta_move(logic: Logic):
        max_move = None
        max_val = -1000
        # actual alpha_beta:
        for child in logic.game_state.possible_moves:
            if len(logic.game_state.board.get_empty_fields()) > 50:
                mini_max = Alpha_Beta.alpha_beta(logic, logic.game_state.perform_move(child), 2, max_val, 100)
            else:
                mini_max = Alpha_Beta.alpha_beta(logic, logic.game_state.perform_move(child), 1, max_val, 100)
            val = mini_max
            if val > max_val:
                max_move = child
                max_val = val
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

    def fish_evaluate(logic: Logic, state: GameState) -> int:
        try:
            if (logic.game_state.current_team.name == logic.game_state.first_team.name):
                return state.first_team.fish - state.second_team.fish
            return state.second_team.fish - state.first_team.fish
        except ValueError:
            logging.error(f"Value Error: current_team: {logic.game_state.current_team.name}")
            return 0

    def alpha_beta(logic: Logic, new_state: GameState, depth: int, alpha, beta, memo : dict = {}):
        '''
        `alpha_beta_fish()` only uses the `fish` value for the evaluation aswell as the `possible_moves`

        Arguments needed are:
            - `GameState`using the new calculated GameState
            - `depth`    defining the depth of the algorithm
            - `alpha`    for the biggest value achieved during the algorithm
            - `beta`     for the smallest value achieved during the algorithm
            - `memo`     used as a memory `dict` to remember similar paths
        '''
        logging.info("ALPHA BETA")
        hash_list = Alpha_Beta.move_hash(new_state)
        value = Alpha_Beta.fish_evaluate(logic, new_state)
        if hash_list in memo:
            return memo[hash_list]

        if depth == 0 or new_state.current_team == None:
            return value #  value berechnen

        maximizing = (new_state.current_team.name == logic.game_state.current_team.name)
        if maximizing:
            if new_state.possible_moves == []:
                return value

            maxEval = -100 # replacement (- inf)
            for child in new_state.possible_moves:
                eval = Alpha_Beta.alpha_beta(logic, new_state.perform_move(child), depth - 1, alpha, beta, memo)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            memo[hash_list] = maxEval
            return maxEval

        else:
            minEval = 100 # replacement (- inf)
            for child in new_state.possible_moves:
                eval = Alpha_Beta.alpha_beta(logic, new_state.perform_move(child), depth - 1, alpha, beta, memo)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            memo[hash_list] = minEval
            return minEval

class Intersection():

    def get_intersection_move(logic: Logic):
        logging.info("INTERSECT, Turn:" + str(logic.game_state.turn))
        logging.info("Intersection:" + str(logic.inters_to))
        moves1 = Intersection.intersections_info_list(logic, logic.game_state.current_team)
        moves2 = Intersection.intersections_info_list(logic, logic.game_state.other_team)
        intersects = Intersection.get_intersections(moves1, moves2)
        best_val: int = 0
        best_move: Move = logic.game_state.possible_moves[0]
        #logging.info(f" \n Moves1: \n {moves1} \n Moves2: \n {moves2} \n Intersects: \n {intersects}")
        for each in intersects:
            val = Intersection.intersect_evaluate(logic, each)
            if val > best_val:
                best_move = each[0][0]
                best_val = val
        return best_move
    
    def intersect_evaluate(logic: Logic, intersection) -> Move:
        turn_add = 1 if logic.game_state.turn <= 8 else 0
        return len(intersection[0][4]) + turn_add  + len(intersection[1][5]) - len(intersection[1][4]) 
                
    def get_intersections(list1: list[list], list2: list[list]) -> list[list[list, list]]:
        result = []
        for l1 in list1:
            for l2 in list2:
                if l1[1] == l2[1]: result.append([l1, l2])
        return result
        
    def get_norm_from_vector(vector: Vector) -> Vector:
        arc = vector.get_arc_tangent()
        direction = None
        for xdir in Vector().directions:
            direction = xdir if arc == xdir.get_arc_tangent() else direction
        return direction

    def intersections_info_list(logic: Logic, team: Team) -> list:
        poss_moves = []
        for p in team.get_penguins():
            for v in Vector().directions:
                moves: list = []
                for i in range(1, 8):
                    destination : HexCoordinate = p.coordinate.add_vector(v.scalar_product(i))
                    if logic.game_state.board._is_destination_valid(destination):
                        move = Move(team_enum=team.name, from_value = p.coordinate, to_value=destination)        
                        vector = Vector(move.to_value.x - move.from_value.x, move.to_value.y - move.from_value.y)   
                        direction = Intersection.get_norm_from_vector(vector)                                            
                        betweens = []
                        for b in moves:                                                                             
                            betweens.append(b[1])
                        moves.append([move, destination, vector, direction, betweens])
                        #logging.info("moves",moves)
                    else:   # If out of bounds
                        break
                
                for a in range(len(moves)):
                    afters = []
                    for b in moves[a + 1:]:
                        afters.append(b[1])
                    moves[a].append(afters)
            
                poss_moves.extend(moves)
                #logging.info(poss_moves)
        #logging.info(poss_moves)
        return poss_moves