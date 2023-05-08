from socha import *

from logic import Logic
from utils.joins import Joins
from extention.board_extentions import *
from extention.print_extentions import *
class Intersection():

    def get_delta_cut_move(logic: Logic):
        max_val = -1000
        max_move: Move = None
        left_inters = Joins.left_inner_join_on(logic.game_state.possible_moves, get_possible_movements(logic.game_state, logic.game_state.current_team.opponent.name), "to_value", False)
        if left_inters == []:
            left_inters = logic.game_state.possible_moves
        for move in left_inters:
            perform = logic.game_state.perform_move(move)
            val = Intersection.delta_fish_possibles(logic, perform)
            if val > max_val:
                max_val = val
                max_move = move
        return max_move

    def delta_possibles(logic: Logic, state: GameState) -> int: #could work with a non-quantonian function
        '''
        `delta_cut` returns the discrepancy of the current's `.possible_moves` and the opponent's `possible_moves`
        '''
        if (logic.game_state.current_team.name == logic.game_state.first_team.name):
            val = len(get_possible_movements(state, logic.game_state.first_team.name)) - len(get_possible_movements(state, logic.game_state.second_team.name))
        else:
            val = len(get_possible_movements(state, logic.game_state.second_team.name)) - len(get_possible_movements(state, logic.game_state.first_team.name))
        return val
    
    def cut_eval(logic: Logic, state: GameState) -> int: #could work with a non-quantonian function
        '''
        '''
        if (logic.game_state.current_team.name == logic.game_state.first_team.name):
            val = -len(get_possible_movements(state, logic.game_state.second_team.name))
        else:
            val = -len(get_possible_movements(state, logic.game_state.first_team.name))
        return val

    def delta_fish_possibles(logic:Logic, state: GameState) -> int:
        '''
        `delta_cut` returns the discrepancy of current's `fish` and the opponent's `fish`
        '''
        if (logic.game_state.current_team.name == logic.game_state.first_team.name):
            max = sum([state.board.get_field(move.to_value).fish for move in get_possible_movements(state, logic.game_state.first_team.name)])
            min = sum([state.board.get_field(move.to_value).fish for move in get_possible_movements(state, logic.game_state.second_team.name)])
        else:
            min = sum([state.board.get_field(move.to_value).fish for move in get_possible_movements(state, logic.game_state.first_team.name)])
            max = sum([state.board.get_field(move.to_value).fish for move in get_possible_movements(state, logic.game_state.second_team.name)])
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
        
        for penguin in team.penguins:   # jeder pinguin
            inters_to = [each.from_value for each in move_list] # alle from values in move_list
            if penguin.coordinate in inters_to:   #if the penguin has no intersection
                penguin_moves = [each for each in move_list if each.from_value == penguin.coordinate]
                penguin_missing_dir : List[Vector] = Vector().directions    #beinhaltet alle richtungen

                for move in penguin_moves:  #richtungen in der der pinguin schon einen move hat
                    direction = get_dir_(Vector(move.to_value.x - move.from_value.x, move.to_value.y - move.from_value.y))
                    if direction in penguin_missing_dir:
                        penguin_missing_dir.remove(direction)

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