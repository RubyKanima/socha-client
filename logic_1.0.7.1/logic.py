from socha import *
from joins import Joins
from socha_extentions import *
import random

class Logic(IClientHandler):

    def __init__(self):
        self.game_state: GameState
        self.all_fields: list[Field]
        self.other_possible_moves: list[Move]
        self.inters: list[list[Move, Move]]
        self.inters_to: list

    def on_update(self, state: GameState):
        self.game_state = state
        self.all_fields = self.game_state.board.get_all_fields()
        self.other_possible_moves = self.game_state._get_possible_moves(self.game_state.current_team.opponent)
        self.game_state.board.get_all_fields()
        self.inters = Joins.inner_join_on(self.game_state.possible_moves, self.other_possible_moves, "to_value", False)
        self.inters_to = Joins.inner_join_on(self.game_state.possible_moves, self.other_possible_moves, "to_value", True)

    def calculate_move(self) -> Move:
        if not self.other_possible_moves:
            return Depth_Search.get_depth_move(self)
        if self.inters_to == []:
            return Alpha_Beta.get_alpha_beta_move(self)
        if self.game_state.turn > 8:
            return Intersection.get_intersection_move(self)
        else:
            return random.choice(self.game_state.possible_moves)

if __name__ == "__main__":
    Starter(Logic())