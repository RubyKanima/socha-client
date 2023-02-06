import random
from tabulate import tabulate

from socha import *


class Logic(IClientHandler):
    game_state: GameState

    def calculate_move(self) -> Move:
        possible_moves = self.game_state.possible_moves
        return possible_moves[random.randint(0, len(possible_moves) - 1)]

    def on_update(self, state: GameState):
        self.game_state = state

def debug(self):
        table = []
        headers =["parameter", "value", "type"]
        print("\n ---------------------- GAMESTATE ---------------------- \n")
        
        for all in self.game_state.__dict__:
            if all not in ["first_team.", "second_team", "possible_moves", "board"]:
                table.append((all, self.game_state.__dict__[all], type(self.game_state.__dict__[all])))
            if all == "first_team":
                for ell in self.game_state.first_team.__dict__:
                    table.append(("first_team."+ell, self.game_state.first_team.__dict__[ell], type(self.game_state.first_team.__dict__)))
            if all == "second_team":
                for ell in self.game_state.second_team.__dict__:
                    table.append(("second_team."+ell, self.game_state.second_team.__dict__[ell], type(self.game_state.second_team.__dict__)))
            if all == "possible_moves":
                for ell in self.game_state.possible_moves:
                    table.append(("possible_move",ell, type(self.game_state.__dict__[all])))

        print(tabulate(table, headers=headers))

if __name__ == "__main__":
    Starter(logic=Logic())