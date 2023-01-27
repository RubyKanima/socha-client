import random
import copy
import time
from tabulate import tabulate
from socha import *


class Logic(IClientHandler):
    game_state: GameState

    def calculate_move(self) -> Move:
        
        print(self.simulate_perform_move(self.game_state, self.game_state.possible_moves[random.randint(0, len(self.game_state.possible_moves) - 1)]))
        """print("- board -")
        print("get field: ", self.game_state.board.get_field(HexCoordinate(1, 1)))
        print("- current pieces -")
        print(self.game_state.current_pieces)
        print("- fishes -")
        print("ONE: ",self.game_state.fishes.fishes_one)
        print("TWO: ",self.game_state.fishes.fishes_two)
        print("- other team -")
        print("other team: ",self.game_state.other_team)
        print("opponent: ", self.game_state.other_team.opponent)
        print("last move: ",self.game_state.last_move)
        print("")"""

        def greedy():
            most_fish = [0, 0]
            for i in self.game_state.possible_moves:
                if i.from_value != None:
                    field = self.game_state.board.get_field(i.to_value)

                    if field.get_fish() != None and field.get_fish() > most_fish[1]:
                        most_fish[0] = i
                        most_fish[1] = field.get_fish()
            return most_fish[0] if most_fish[0] != 0 else self.game_state.possible_moves[random.randint(0, len(self.game_state.possible_moves) - 1)]
        
        #def evaluate(new_board: Board, ):
            #own_fish = self.game_state.fishes.get_fish_by_team(self.game_state.current_team.team())
            #enemy_fish = self.game_state.fishes.get_fish_by_team(self.game_state.other_team.team())
            #return own_fish - enemy_fish + extra_fish

        def mini_max( depth: int, maximizing: bool, new_state: GameState, new_move: Move): #
            if depth == 0 or new_state.board.possible_moves_from(new_move.to_value) == []: 
                return self.evaluate(new_state) #  value berechnen
            if maximizing:
                maxEval = -100000 # replacement (- inf)
                for child in new_state.board.possible_moves_from(new_move.to_value): #possible_moves is wrong
                    eval = mini_max(child,depth - 1, False)
                    maxEval = max(maxEval,eval)
                return maxEval
            else:
                minEval = 100000 # replacement (- inf)
                for child in new_state.board.possible_moves_from(new_move.to_value): #possible_moves is wrong
                    eval = mini_max(child,depth - 1, True)
                    minEval = min(minEval,eval)
                return minEval
        '''INITIALIZATIONS'''
        #evaluate()
        self.debug()
        self.get_map(state = self.game_state)
        print("\n --------------------------------------------------- \n")
        if (self.game_state.last_move != None):
            self.get_map(self.game_state)
            #print(map)
        # -> return possible_moves[random.randint(0, len(possible_moves) - 1)]
        return greedy()
    '''---------------'''
    def get_map(self, state: GameState) ->Board:
        new_board = []
        #TEST
        turn = state.turn
        print("#-#", state.turn)
        turn += 1
        print("#-#",turn, "||", state.turn)
        #TEST
        for y in state.board._game_field:
            new_board.append([])
            for x in y:
                new_board[-1].append(x)
        return Board(new_board)

    def print_map(self, state: GameState):

        for y in range(0,8):
            line = ""
            for x in range(0,8):
                value = str(state.board._get_field(x,y).get_value())
                line +="  .  ".replace(".",value) if type(value) == int else "  .  ".replace(" . ",value)
            if y%2 == 1:
                print(" ",line) 
            else:
                print(line)
            
    def simulate_perform_move(self, state: GameState, move: Move, add_turn: bool = True) -> GameState:

        if state.is_valid_move(move):
            new_state = copy.deepcopy(state)
            add_fish = state.board.get_field(move.to_value).get_fish()
            new_state.board = self.simulate_move(state,move)
            new_state.turn +=1 if add_turn else 0
            if state.current_team == Team('ONE'): new_state.fishes.fishes_one += add_fish
            else: new_state.fishes.fishes_two += add_fish
            return new_state

        raise Exception(f"Invalid move: {move}")

    def simulate_move(self, state: GameState, move: Move) -> Board:
        new_board : Board = self.get_map(state)
        to_coordinate = move.to_value.to_cartesian()
        new_board._game_field[to_coordinate.y][to_coordinate.x].field = state.current_team.color()
        if move.from_value != None:
            from_coordinate = move.from_value.to_cartesian()
            new_board._game_field[from_coordinate.y][from_coordinate.x].field = 0
        return new_board

    def on_update(self, state: GameState):

        self.game_state = state
        tile1 = Tile(0)
        tile2 = copy.copy(tile1)
        tile1.debug()
        def test_print(new_tile: Tile):
            new_tile.i = 4
            print(new_tile.i, "||", tile1.i)
        test_print(tile1)
    def debug(self):
        table = []
        headers =["parameter", "value", "type"]
        print("\n ---------------------- GAMESTATE ---------------------- \n")
        
        for all in self.game_state.__dict__:
            if all not in ["fishes", "possible_moves", "board"]:
                table.append((all, self.game_state.__dict__[all], type(self.game_state.__dict__[all])))
            if all == "fishes":
                for ell in self.game_state.fishes.__dict__:
                    table.append(("fishes."+ell, self.game_state.fishes.__dict__[ell], type(self.game_state.fishes.__dict__)))
            if all == "possible_moves":
                for ell in self.game_state.possible_moves:
                    table.append(("possible_move",ell, type(self.game_state.__dict__[all])))

        print(tabulate(table, headers=headers))
        print("\n --------------------------------------------------- \n")
logic = Logic()

"""New Classes"""
class Tile():
    game_state: GameState
    hex: HexCoordinate
    def __init__(self, i):
        self.i = i
        self.field = logic.game_state.board.get_field_by_index(self.i)
        self.fish = self.field.get_fish()
        self.neighbors_sum = sum(self.get_neighbor_fish())
        print("--", self.get_valid_neighbors())
        self.debug()

    def get_valid_neighbors(self):
        valid_neighbors = []
        for all in HexCoordinate.get_neighbors(self.field.coordinate):
            if logic.game_state.board.is_valid(all) and not logic.game_state.board.is_occupied(all): valid_neighbors.append(all)
        return valid_neighbors

    def get_neighbor_fish(self):
        tmp_list = []
        for all in self.get_valid_neighbors():
            tmp_list.append(logic.game_state.board.get_field(all).get_fish())
            print(all.x, all.y,"-", all.to_cartesian()," : ",logic.game_state.board.get_field(all).get_fish())
        return tmp_list

    def debug(self):
        table = []
        headers =["parameter", "value", "type"]
        print("\n ---------------------- TILES ---------------------- \n")
        for all in self.__dict__:
            if all not in ["field"]:
                table.append((all, self.__dict__[all], type(self.__dict__[all])))
            else:
                for ell in self.__dict__[all].__dict__:
                    table.append((all+"."+ell, self.__dict__[all].__dict__[ell], type(self.__dict__[all].__dict__[ell])))
        print(tabulate(table, headers=headers))
        print("\n --------------------------------------------------- \n")
"""-----------"""
if __name__ == "__main__":
    Starter(logic)

