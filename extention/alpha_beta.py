from socha import *
from logic import Logic
from .triangles import *
from .board_extentions import *
class AlphaBeta():
    
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
    
    def get_tri_alpha_move(logic: Logic):
        max_val = -1000
        max_move: Move = logic.game_state.possible_moves[0]
        move_list = []
        if logic.game_state.turn > 8:
            penguins = logic.tri_board.get_contesting_penguins()
            
            for penguin in penguins:
                #print(penguin)
                if penguin.team_enum.name == logic.game_state.current_team.name.name:
                    move_list.extend(logic.game_state.board.possible_moves_from(penguin.coordinate))
        else:
            move_list = logic.game_state.possible_moves
        
        for each in move_list:
            mini_max = AlphaBeta.tri_alpha(logic.tri_board.perform_move(each), logic.game_state.current_team, 0, logic.tri_board.board.get_field(each.to_value).fish, False, max_val, 1000)
            val = mini_max
            if val > max_val:
                max_move = each
                max_val = val
        return max_move
    
    def tri_alpha(tri_board: TriBoard, global_team: Team, depth: int, fish: int, maximizing:bool, alpha: int, beta:int):
        
        move_list = get_possible_moves_from_team(tri_board.board, tri_board.current_team.name)

        if not tri_board.is_any_contest() or depth == 0 or not move_list:
            return AlphaBeta.tri_eval2(tri_board, global_team) + fish + AlphaBeta._get_move(tri_board, move_list, global_team)
            
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
    
    def tri_eval2(tri_board: TriBoard, global_team: Team):
        check_list = {}
        for group in tri_board.groups():
            for key in group.group:
                check_list[key] = group.group[key].fish

        own_coords = [each.coordinate for each in tri_board.board.get_teams_penguins(global_team.name)]
        other_coords = [each.coordinate for each in tri_board.board.get_teams_penguins(global_team.opponent.name)]
        
        own_value = AlphaBeta.get_depth_possibles(tri_board.board, check_list.copy(), own_coords)
        other_value = AlphaBeta.get_depth_possibles(tri_board.board, check_list.copy(), other_coords)
        return own_value - other_value
    
    def tri_eval_print(tri_board: TriBoard, global_team: Team):
        check_list = {}
        for group in tri_board.groups():
            if group.is_contesting():
                for key in group.group:
                    check_list[key] = group.group[key].fish

        own_coords = [each.coordinate for each in tri_board.board.get_teams_penguins(global_team.name)]
        other_coords = [each.coordinate for each in tri_board.board.get_teams_penguins(global_team.opponent.name)]
        
        own_value = AlphaBeta.get_depth_possibles(tri_board.board, check_list.copy(), own_coords)
        other_value = AlphaBeta.get_depth_possibles(tri_board.board, check_list.copy(), other_coords)

        own_value2 = 0
        other_value2 = 0
        for group in tri_board.groups():
            if group.is_contesting() or group.penguins == []:
                continue
            if group.penguins[0].team_enum.name == global_team.name.name:
                own_value2 += group.fish
            else:
                other_value2 -= group.fish
        

        print(own_value, -other_value, own_value2, other_value2)

    def get_depth_possibles(board: Board, check_list: dict[str, Tile], check_coords: list[HexCoordinate]):
        

        value = 0
        iteration = 1
        while check_coords:
            destinations = []
            for coord in check_coords:
                for direction in Vector().directions:
                    for i in range(1,8):
                        destination = coord.add_vector(direction.scalar_product(i))
                        this_hash = own_hash(destination)
                        if this_hash in check_list:
                            value += check_list[this_hash] / iteration
                            check_list.pop(this_hash)
                            destinations.append(destination)
                        elif not board._is_destination_valid(destination):
                            break
                        else: 
                            continue
            check_coords = destinations
            iteration+=1
        return value
    
    def _get_move(tri_board: TriBoard, possible_moves: list[Move], global_team: Team):
        max_val = -1000
        max_move = possible_moves[0]
        move_list = possible_moves
        move_list = [move for move in move_list if tri_board.tri_board()[move.to_value.x>>1][move.to_value.y].spot == "white" or tri_board.tri_board()[move.to_value.x>>1][move.to_value.y].spot == "yellow"]
        #print_moves_board_custom(logic.game_state.board , move_list, one_char="B", two_char="E")
        
        this_team = global_team.opponent if global_team.name.name != possible_moves[0].team_enum.name else global_team

            
        for move in move_list:
            val = AlphaBeta.get_fish_evaluate(tri_board.board, move.to_value, this_team)
            if val >= max_val:
                max_val = val
        
        if global_team.name.name == possible_moves[0].team_enum.name:
            return max_val
        else:
            return -max_val

    def get_move(logic: Logic):
        max_val = -1000
        max_move = logic.game_state.possible_moves[0]
        move_list = logic.game_state.possible_moves
        move_list = [move for move in move_list if logic.tri_board.tri_board()[move.to_value.x>>1][move.to_value.y].spot == "white" or logic.tri_board.tri_board()[move.to_value.x>>1][move.to_value.y].spot == "yellow"]
        #print_moves_board_custom(logic.game_state.board , move_list, one_char="B", two_char="E")

        for move in move_list:
            val = AlphaBeta.get_fish_evaluate(logic.game_state.board, move.to_value, logic.game_state.current_team)
            if val >= max_val:
                max_val = val
                max_move = move
        return max_move
    
    def get_fish_evaluate(board: Board, origin: HexCoordinate, global_team: Team):
        value = 0
        #other_possibles = get_possible_moves_from_team(board, global_team.opponent.name)
        #intersections = AlphaBeta.get_first_inters_from_with(board, origin, other_possibles)
        for direction in Vector().directions:
            factor = 1
            for i in range(1,8):
                destination = origin.add_vector(direction.scalar_product(i))
                if not own_is_valid(destination):
                    break

                if board.get_field(destination).fish == 0:
                    break
                value += board.get_field(destination).fish * factor
        return value
    
    def get_first_inters_from_with(board: Board, origin: HexCoordinate, other_list: list[Move]) ->list[HexCoordinate]:
        first_intersections = []
        for direction in Vector().directions:
            stop = False
            for i in range(1, 8):
                if stop: 
                    break 
                destination = origin.add_vector(direction.scalar_product(i))
                if not own_is_valid(destination):
                    break
                if board.get_field(destination).fish != 0: # stop if end of board/ axis
                    for each in other_list: # add move if intersect
                        if destination == each.to_value:
                            first_intersections.append(each.to_value)
                            stop = True
                            break   # stop at first instance
                else:
                    break
        return first_intersections