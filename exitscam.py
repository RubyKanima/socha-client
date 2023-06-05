from socha import *
from extention import *

class Logic(IClientHandler):

    # //////////////// standard logic ////////////////

    game_state: GameState

    def __init__(self):

        self.init = False

    def calculate_move(self) -> Move:

        self.tri_board = TriBoard(self.game_state.board, self.game_state.current_team, [], [], [])
        print_common(self.game_state.board, self.game_state.current_team.name.name)
        self.tri_board.__own_repr__()
        logging.info(self.game_state.turn)
        
        if not self.init:

            self.copy_mode = True if self.game_state.current_team.name.name == 'TWO' else False
            print("Copy Mode", self.copy_mode)

            self.init = True

        self.copy_move = self.copy()

        if self.game_state.turn < 8:
            print("COPY 1")
            return self.copy()
        
        if self.copy_move:
            if self.josef_stupid():
                print("SMART WEIL JOSEF STUPID")
                return self.smart_sein()
        
            print("COPY 2")
            return self.copy()
        
        print("SMART WEIL NICHTS ANDERES")
        self.smart_sein()


    def on_update(self, state: GameState):
        self.game_state = state

    
    def copy(self):

        lm = self.game_state.last_move

        if lm == None:
            return None

        cart_from = None if lm.from_value == None else lm.from_value
        cart_to = lm.to_value

        invert_from = None if cart_from == None else HexCoordinate(15 - cart_from.x, 7 - cart_from.y)
        invert_to = HexCoordinate(15 - cart_to.x, 7 - cart_to.y)

        copy_move = Move(self.game_state.current_team.name, invert_from, invert_to)

        if copy_move in self.game_state.possible_moves:
            return copy_move

        return None
    
    def josef_stupid(self):
        # returns True if josef stupid aka he does move in not contesting

        group = self.tri_board.tri_board[self.copy_move.to_value.to_cartesian().y][self.copy_move.to_value.to_cartesian().x].group

        return not self.tri_board.groups[group].is_contestet()
    
    def smart_sein(self):

        contest = False
        for g in self.tri_board.groups:
            if g.is_contestet():
                contest = True
                break

        if not contest:
            print("tri")
            return self.tri_board.get_least_shapes_move(self)

        print("a-b")
        return AlphaBeta.get_alpha_beta_cut_move(self)


if __name__ == "__main__":
    Starter(Logic())
