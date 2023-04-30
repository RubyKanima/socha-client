from socha import *
from socha_algorithms import *
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
        if self.game_state.turn < 8:                            # Beginning Moves
            logging.info("most_possible_move")
            return Alpha_Beta.get_most_possible_move(self)
        if not self.other_possible_moves:                       # Following Moves if the enemies don't matter
            logging.info("get_alpha_beta_cut_move")
            return Alpha_Beta.get_alpha_beta_cut_move(self)
        if not self.inters_to == []:                            # Following Moves against enemy
            logging.info("get_alpha_beta_cut_move")
            return Alpha_Beta.get_alpha_beta_cut_move(self)
        if self.inters_to == []:                                # Following Moves if no moves possible against enemies
            logging.info("get_alpha_beta_cut_move")
            return Alpha_Beta.get_alpha_beta_cut_move(self)
        if not self.game_state.possible_moves == []:            # Following Moves if he is clueles
            logging.error("UNAVOIDABLE ERROR")
            return random.choice(self.game_state.possible_moves)
        else:                                                   # No Move possible
            return None
if __name__ == "__main__":
    Starter(Logic())