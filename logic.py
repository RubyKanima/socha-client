from socha import *

#import logging
from random import choice
from extention import *

class Logic(IClientHandler):
    def __init__(self):     
        self.game_state: GameState
        self.tri_board: TriBoard
        self.copy: bool = True

    def on_update(self, state: GameState):
        self.game_state = state    
        print(self.game_state.turn)
        #logging.info(str(self.game_state.first_team.fish)+" "+ str(self.game_state.second_team.fish))
       
    def calculate_move(self):
        print(self.game_state.current_team)
        self.tri_board = TriBoard(self.game_state.board, self.game_state.current_team, [], [], [])
        self.copy = True if self.game_state.current_team.name.name == "TWO" and self.copy else False
        copy_move: Move
        if self.copy:
            #print(self.copy)
            copy_move = copycat(self.game_state.last_move, self.game_state.current_team.name)
            self.copy = copycat_validity(copy_move, self.tri_board) if self.game_state.turn > 1 else True
            self.copy = True if copy_move in self.game_state.possible_moves else False
        if self.copy:
            return copy_move        
        
        AlphaBeta.tri_eval_print(self.tri_board, self.game_state.current_team)
        #print(AlphaBeta.tri_eval2(self.tri_board, self.game_state.current_team))
    
        if self.game_state.turn == 0:
            return AlphaBeta.get_most_possible_fish_move(self)

        if not self.tri_board.is_any_contest():                       # Following Moves if the enemies don't matter
            #logging.info("least")
            return self.tri_board.get_least_shapes_move(self)
        
        if self.tri_board.is_any_contest():                            # Following Moves against enemy
            #logging.info("tri_alpha")
            return AlphaBeta.get_tri_alpha_move(self)
            #return AlphaBeta.get_move(self)

        #logging.error("UNAVOIDABLE ERROR")
        return choice(self.game_state.possible_moves)
        
if __name__ == "__main__":
    Starter(Logic())
