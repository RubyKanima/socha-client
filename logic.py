from socha import *

import logging
import random

from extention import *
from utils import *


class Logic(IClientHandler):
    def __init__(self):     
        self.game_state: GameState

    @property
    def other_possible_moves(self):
         if not self.game_state.current_team == None:
            if not self.game_state.current_team.opponent == None:
                return self.game_state._get_possible_moves(self.game_state.current_team.opponent)

    @property
    def all_field(self):
        return self.game_state.board.get_all_fields()

    @property
    def inters_to(self):
        if not self.other_possible_moves == [] and not self.game_state.possible_moves == []:
            return Joins.inner_join_on(self.game_state.possible_moves, self.other_possible_moves, "to_value", True)

    def on_update(self, state: GameState):
        self.game_state = state
       
    def calculate_move(self):
        logging.info(self.game_state.turn)

        if self.game_state.turn < 8:                            # Beginning Moves
            logging.info("most_possible_move")
            return Alpha_Beta.get_most_possible_move(self)
        
        if not self.other_possible_moves:                       # Following Moves if the enemies don't matter
            logging.info("least")
            return Alpha_Beta.get_least_neighbor_move(self)
        
        if not self.inters_to:                            # Following Moves against enemy
            logging.info("least2")
            return Alpha_Beta.get_least_neighbor_move(self)
        
        if self.inters_to:                                # Following Moves if no moves possible against enemies
            logging.info("get_alpha_beta_cut_move")
            return Alpha_Beta.get_alpha_beta_cut_move(self)
    
        logging.error("UNAVOIDABLE ERROR")
        return random.choice(self.game_state.possible_moves)
        
logic = Logic()

if __name__ == "__main__":
    Starter(logic)

