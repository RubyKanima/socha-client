from socha import *
from socha_algorithms import *
from socha_extentions import *
from joins import Joins
import logging
import random

class Logic(IClientHandler):
    def __init__(self):     
        self.game_state: GameState
        self.all_fields: list[Field]
        self.other_possible_moves: list[Move]
        #self.full_inters: list[list[Move, Move]]
        #self.left_inters: list[Move]
        self.inters_to: list

    def on_update(self, state: GameState):
        self.game_state = state
        self.all_fields = self.game_state.board.get_all_fields()
        if not self.game_state.current_team == None:
            if not self.game_state.current_team.opponent == None:
                self.other_possible_moves = self.game_state._get_possible_moves(self.game_state.current_team.opponent)
        self.game_state.board.get_all_fields()
        if not self.other_possible_moves == [] and not self.game_state.possible_moves == []:
            #self.full_inters = Joins.inner_join_on(self.game_state.possible_moves, self.other_possible_moves, "to_value", False)
            #self.left_inters = [each[0] for each in self.full_inters]
            self.inters_to = Joins.inner_join_on(self.game_state.possible_moves, self.other_possible_moves, "to_value", True)

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

