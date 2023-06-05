from socha import *

class Logic(IClientHandler):

    # //////////////// standard logic ////////////////

    gameState: GameState

    def __init__(self):

        self.init = False

    def calculate_move(self) -> Move:
        
        if not self.init:

            self.copy_mode = True if self.gameState.current_team.name.name == 'TWO' else False
            print(self.copy_mode)

            self.init = True

        move = self.gameState.possible_moves[0]

        if self.copy_mode:

            if self.josef_stupid():
                pass # smart move

            else:
                c = self.copy()
                move = self.copy() if c else move
        
        return move

    def on_update(self, state: GameState):
        self.gameState = state

    
    def copy(self):

        lm = self.gameState.last_move

        if lm == None:
            return None

        cart_from = None if lm.from_value == None else lm.from_value.to_cartesian()
        cart_to = lm.to_value.to_cartesian()

        invert_from = None if cart_from == None else CartesianCoordinate(7 - cart_from.x, 7 - cart_from.y).to_hex()
        invert_to = CartesianCoordinate(7 - cart_to.x, 7 - cart_to.y).to_hex()

        copy_move = Move(self.gameState.current_team.name, invert_from, invert_to)

        if copy_move in self.gameState.possible_moves:
            return copy_move

        return None
    
    def josef_stupid(self):

        return False


if __name__ == "__main__":
    Starter(Logic())
