from socha import *
from socha_extentions import *
from joins import Joins
from typing import List, Optional, Any
import logging
import random

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
        if self.game_state.turn < 2:                            # Beginning Move
            logging.info("most_possible_move")
            return Alpha_Beta.get_most_possible_move(self)
        if not self.inters_to == []:                            # Following Moves against enemy
            logging.info("get_alpha_beta_cut_move")
            return Alpha_Beta.get_alpha_beta_cut_move(self)
        if self.inters_to == []:                                # Following Moves if no moves possible against enemies
            logging.info("get_alpha_beta_fish_move")
            return Alpha_Beta.get_alpha_beta_fish_move(self)
        if not self.other_possible_moves:                       # Following Moves if the enemies don't matter
            logging.info("_get_depth_move")
            return Tree._get_depth_move(self)
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
        logging.info(f"\n team, penguins: {team, penguins} \n")
        for penguin in penguins:
            possible_movements.extend(state.board.possible_moves_from(penguin.coordinate, penguin.team_enum))
        return possible_movements
    
if __name__ == "__main__":
    Starter(Logic())