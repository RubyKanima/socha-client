from socha import *
from socha_extentions import *
from joins import Joins
from typing import List, Optional, Any
from tabulate import tabulate
import logging
import random

import cProfile
import pstats

class Logic(IClientHandler):
    def __init__(self):     
        self.game_state: GameState
        self.all_fields: list[Field]
        self.other_possible_moves: list[Move]
        self.full_inters: list[list[Move, Move]]
        self.left_inters: list[Move]
        self.inters_to: list

    def on_update(self, state: GameState):
        self.game_state = state
        self.all_fields = self.game_state.board.get_all_fields()
        if not self.game_state.current_team == None:
            if not self.game_state.current_team.opponent == None:
                self.other_possible_moves = self.game_state._get_possible_moves(self.game_state.current_team.opponent)
        self.game_state.board.get_all_fields()
        if not self.other_possible_moves == [] and not self.game_state.possible_moves == []:
            self.full_inters = Joins.inner_join_on(self.game_state.possible_moves, self.other_possible_moves, "to_value", False)
            self.left_inters = [each[0] for each in self.full_inters]
            self.inters_to = Joins.inner_join_on(self.game_state.possible_moves, self.other_possible_moves, "to_value", True)

    def calculate_move(self) -> Move:
        """with cProfile.Profile() as pr:
            self.calc()
        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()"""
        return self.calc()
        
    def calc(self):
        if self.game_state.turn < 4:                            # Beginning Moves
            logging.info("most_possible_move")
            return Alpha_Beta.get_most_possible_move(self)
        if not self.inters_to == []:                            # Following Moves against enemy
            logging.info("get_alpha_beta_cut_move")
            return Alpha_Beta.get_alpha_beta_cut_move(self)
        if self.inters_to == []:                                # Following Moves if no moves possible against enemies
            logging.info("get_alpha_beta_fish_move")
            return Alpha_Beta.get_alpha_beta_fish_move(self)
        if not self.other_possible_moves:                       # Following Moves if the enemies don't matter
            logging.info("get_alpha_beta_fish_move")
            return Alpha_Beta.get_alpha_beta_fish_move(self)
            '''
            logging.info("_get_depth_move")
            return Tree._get_depth_move(self)
            '''
        if not self.game_state.possible_moves == []:            # Following Moves if he is clueles
            return random.choice(self.game_state.possible_moves)
        else:                                                   # No Move possible
            return None
        
        '''
        # isnt working properly
        if not self.other_possible_moves:
            return self.max_move(self.game_state.possible_moves, Tree._depth) #should work
        if self.inters_to == []:
            # return self.max_move(self.game_state.possible_moves, Alpha_Beta.alpha_beta_fish, 3, ) # needs check
            return self.max_move(Joins.inner_join_on, self.game_state, Alpha_Beta.alpha_beta, self)
        if self.game_state.turn > 8 and not self.inters_to == []:
            return self.max_move(self.inters, Intersection.delta_possibles)
        else:
            return random.choice(self.game_state.possible_moves)
            '''
        
    def max_move(list_f, state: GameState, evaluate_f, logic: Optional[Any] = None, depth: Optional[int] = None, extra_f : Optional[Any] = None):
        '''
        is malfunctioning because of the given attributes and incompatible Logic !
        '''
        
        max_val: int = 0
        max_move: Move
        _list: List[Move] = list_f(state)
        move_list: List[Move] = _list if type(list_f) is not list else list_f #dangerous
        
        if evaluate_f is Alpha_Beta.alpha_beta:
            for move in move_list:
                val: int = evaluate_f(logic, state.perform_move(move), depth, list_f, extra_f)
                if val > max_val:
                    max_move = move
                    max_val = val

        else:
            for move in move_list:
                val: int = evaluate_f(state.perform_move(move))
                if val > max_val:
                    max_move = move
                    max_val = val
        return max_move
    
    def get_possible_movements(state: GameState, team: TeamEnum = None):
        if team == None:
            team = state.current_team
        possible_movements = []
        penguins: list[Penguin] = state.board.get_teams_penguins(team.name)
        #logging.info(f"\n team, penguins: {team, penguins} \n")
        for penguin in penguins:
            possible_movements.extend(state.board.possible_moves_from(penguin.coordinate, penguin.team_enum))
        return possible_movements
    
    def get_fields_in_direction(board: Board, origin: HexCoordinate, direction: Vector, team_enum: Optional[TeamEnum] = None) -> List[Field]:
        """
        Gets all moves in the given direction from the given origin.

        Args:
            origin: The origin of the move.
            direction: The direction of the move.
            team_enum: Team to make moves for.

        Returns:
                List[Field]: List of moves that can be made in the given direction from the given index,
                            for the given team_enum
        """
        if team_enum is None:
            team_enum = board.get_field(origin).penguin.team_enum
        if not board.get_field(origin).penguin or board.get_field(origin).penguin.team_enum != team_enum:
            return []

        fields = []
        for i in range(1, board.width()):
            destination = origin.add_vector(direction.scalar_product(i))
            if board._is_destination_valid(destination):
                fields.append(board.get_field(destination))
            else:
                break
        return fields
    
    def get_possible_fields_from(state: GameState, position: HexCoordinate, team_enum: TeamEnum = None)-> List[Field]:
        if team_enum == None:
            team_enum = state.current_team.name
        if not state.board.is_valid(position):
            raise IndexError(f"Index out of range: [x={position.x}, y={position.y}]")
        if not state.board.get_field(position).penguin or (
                team_enum and state.board.get_field(position).penguin.team_enum != team_enum):
            return []
        return [field for direction in Vector().directions for field in
                Logic.get_fields_in_direction(state.board, position, direction, team_enum)]

    def get_possible_fields(state: GameState, team: TeamEnum = None)-> List[Field]:
        if team == None:
            team = state.current_team
        possible_fields = []
        penguins: list[Penguin] = state.board.get_teams_penguins(team.name)
        #logging.info(f"\n team, penguins: {team, penguins} \n")
        for penguin in penguins:
            possible_fields.extend(Logic.get_possible_fields_from(state, penguin.coordinate, penguin.team_enum))
        return possible_fields

    def print_moves(list: List[Move]):
        table = [["Team", "From Cart.", "To Cart."]]
        for each in list:
            if each.from_value:
                from_string = str(each.from_value.to_cartesian().x)+", "+str(each.from_value.to_cartesian().y)
            else:
                from_string = "None"
            to_string = str(each.to_value.to_cartesian().x)+", "+str(each.to_value.to_cartesian().y)
            table.append([str(each.team_enum.name),from_string, to_string])
        logging.info("\n" + tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

if __name__ == "__main__":
    Starter(Logic())