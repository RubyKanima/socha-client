from socha import *

import logging
import random

from extention import *
from utils import *

class Logic(IClientHandler):
    def __init__(self):     
        self.game_state: GameState
        self.tri_board: TriBoard

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
            return Joins.left_inner_join_on(self.game_state.possible_moves, self.other_possible_moves, "to_value", True)

    def on_update(self, state: GameState):
        self.game_state = state    
       
    def calculate_move(self):
        self.tri_board = TriBoard(self.game_state.board, self.game_state.current_team, [], [], [])
        print_common(self.game_state.board, self.game_state.current_team.name.name)
        """
        self.tri_board.__own_repr__()
        self.tri_board.__own_sub_repr__()

        print(" ############################# ")
        print(" PERFORM MOVE")
        self.tri_board.perform_move(self.game_state.possible_moves[0]).__own_repr__(self.game_state.current_team.name.name)
        """
        logging.info(self.game_state.turn)

        if self.game_state.turn < 4:                            # Beginning Moves
            logging.info("most_possible_move")
            return AlphaBeta.get_most_possible_move(self)
        
        if self.game_state.turn < 8:
            logging.info("delta_cut")
            return Intersection.get_move(self)
        
        if not self.tri_board.is_any_contest():                       # Following Moves if the enemies don't matter
            logging.info("least")
            logic = self
            return TriBoard.get_least_shapes_move(self.tri_board, logic)
        
        if self.tri_board.is_any_contest():                            # Following Moves against enemy
            logging.info("least2")
            logic = self
            return AlphaBeta.get_tri_alpha_move(logic)
            
        """
        if self.inters_to:                                # Following Moves if no moves possible against enemies
            logging.info("get_alpha_beta_cut_move")
            return Intersection.get_move(self)
        
        if not self.inters_to:
            logging.info("get tri_cut_move")
        """

    
        logging.error("UNAVOIDABLE ERROR")
        return random.choice(self.game_state.possible_moves)
        
if __name__ == "__main__":
    Starter(Logic())

