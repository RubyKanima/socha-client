from socha import *

class Logic(IClientHandler):

    # //////////////// standard logic ////////////////

    gameState: GameState

    def __init__(self):
        pass

    def calculate_move(self) -> Move:

        cart_from = None if self.gameState.last_move.from_value == None else self.gameState.last_move.from_value.to_cartesian()
        cart_to = self.gameState.last_move.to_value.to_cartesian()

        invert_from = None if cart_from == None else CartesianCoordinate(7 - cart_from.x, 7 - cart_from.y).to_hex()
        invert_to = CartesianCoordinate(7 - cart_to.x, 7 - cart_to.y).to_hex()

        copy_move = Move(self.gameState.current_team.name, invert_from, invert_to)

        if copy_move in self.gameState.possible_moves:
            return copy_move
        
        return self.gameState.possible_moves[0]

    def on_update(self, state: GameState):
        self.gameState = state


if __name__ == "__main__":
    Starter(Logic())
