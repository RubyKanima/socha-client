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
            return Joins.inner_join_on(self.game_state.possible_moves, self.other_possible_moves, "to_value", True)

    def on_update(self, state: GameState):
        self.game_state = state    
       
    def calculate_move(self):
        self.tri_board = TriBoard(self.game_state.board, self.game_state.current_team, [], [], [])
        print_common(self.game_state.board, self.game_state.current_team.name.name)
        self.tri_board.__own_repr__()
        logging.info(self.game_state.turn)

        for t in self.tri_board.tri_board:
            print(t)
            print("1", 1)

        print(len(self.tri_board.tri_board))
        '''
        white 0/1
        yellow 0/1
        red 0/1
        black 0/1
        fish linear(1, 4, x)
        group fish sigmoid(1, 80, x)
        score/average score linear(1, 4, x)
        tri inters linear(1, 6, x)
        enemy inters linear(0, 4, x)
        enemy behind sigmoid(0, 12, x)
        enemy between sigmoid(0, 12, x)
        mate inters linear(0, 3, x)
        mate behind sigmoid(0, 12, x)
        mate between sigmoid(0, 12, x)

        instead of plugging fish values into function, plug average fish values
        '''
        
        return random.choice(self.game_state.possible_moves)
        
if __name__ == "__main__":
    Starter(Logic())

