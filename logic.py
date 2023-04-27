from socha import *
import logging
from joins import Joins
from alpha_beta import Alpha_Beta
from socha_extentions import CustomBoard, Tile, Blob

class Logic(IClientHandler):
    def __init__(self):
        self.game_state: GameState
        self.all_fields: list[Field]
        self.opp_possible_moves: list[Move]
        self.inters: list[list[Move, Move]]
        self.inters_to: list

    def on_update(self, state: GameState):
        self.game_state = state
        self.all_fields = self.game_state.board.get_all_fields()
        self.opp_possible_moves = self.game_state._get_possible_moves(self.game_state.current_team.opponent)
        self.game_state.board.get_all_fields()
        self.inters = Joins.inner_join_on(self.game_state.possible_moves, self.opp_possible_moves, "to_value", False)
        self.inters_to = Joins.inner_join_on(self.game_state.possible_moves, self.opp_possible_moves, "to_value", True)

    def calculate_move(self) -> Move:
        logging.info("test")
        logging.info(Joins.inner_join_on(self.game_state.possible_moves, self.opp_possible_moves, "to_value", True))
        Board.pretty_print(CustomBoard.del_fields(self.game_state.board))
        return self.game_state.possible_moves[0]

    def depth_search():
        return "missing function"

if __name__ == "__main__":
    Starter(Logic())