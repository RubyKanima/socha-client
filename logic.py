import random
from socha import *

class Logic(IClientHandler):
    game_state: GameState
    
    def calculate_move(self) -> Move:
        most_fish = [0,0]
        for i in self.game_state.possible_moves:
            if i.from_value != None:
                field = self.game_state.board.get_field(i.to_value)

                if field.get_fish() != None and field.get_fish() > most_fish[1]:
                    most_fish[0] = i
                    most_fish[1] = field.get_fish()
        return most_fish[0] if most_fish[0] != 0 else self.game_state.possible_moves[random.randint(0, len(self.game_state.possible_moves) - 1)]

    def on_update(self, state: GameState):
        self.game_state = state
    
if __name__ == "__main__":
    Starter(logic = Logic())