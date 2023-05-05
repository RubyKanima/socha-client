from socha import *
from socha_algorithms import *
from socha_extentions import *
from joins import Joins
import logging
import random

class Logic(IClientHandler):
    def __init__(self):     
        self.game_state: GameState
        self.all_fields: list[Field]
        self.other_possible_moves: list[Move]
        #self.full_inters: list[list[Move, Move]]
        #self.left_inters: list[Move]
        self.inters_to: list

    def on_update(self, state: GameState):
        self.game_state = state
        self.all_fields = self.game_state.board.get_all_fields()
        if not self.game_state.current_team == None:
            if not self.game_state.current_team.opponent == None:
                self.other_possible_moves = self.game_state._get_possible_moves(self.game_state.current_team.opponent)
        self.game_state.board.get_all_fields()
        if not self.other_possible_moves == [] and not self.game_state.possible_moves == []:
            #self.full_inters = Joins.inner_join_on(self.game_state.possible_moves, self.other_possible_moves, "to_value", False)
            #self.left_inters = [each[0] for each in self.full_inters]
            self.inters_to = Joins.inner_join_on(self.game_state.possible_moves, self.other_possible_moves, "to_value", True)

    def calculate_move(self):
        self.poss_moves = self.game_state.possible_moves
        self.all_fields = self.game_state.board.get_all_fields()
        self.my_team = self.game_state.current_team
        self.op_team = self.my_team.opponent

        logging.info(self.game_state.turn)
        if self.game_state.turn < 8:                            # Beginning Moves
            logging.info("most_possible_move")
            return Alpha_Beta.get_most_possible_move(self)
        if not self.other_possible_moves:                       # Following Moves if the enemies don't matter
            logging.info("least")
            return Alpha_Beta.get_least_neighbor_move(self)
        if not self.inters_to:                            # Following Moves against enemy
            logging.info("least2")
            return Alpha_Beta.get_least_neighbor_move(self)
        if self.inters_to:                                # Following Moves if no moves possible against enemies
            logging.info("get_alpha_beta_cut_move")
            return self.schneider_02()
    
        logging.error("UNAVOIDABLE ERROR")
        return random.choice(self.game_state.possible_moves)
    
    # //////////////// ente ////////////////

    def schneider_02(self) -> Move:

        # if first match's turn:
        if self.game_state.turn < 8: 
            moves1 = []
            for p in self.poss_moves:
                moves1.append({
                    'move': p,
                    'to_value': p.to_value,
                    'vector': None,
                    'direction': None,
                    'between': [],
                    'behind': []
                    })

        else:
            moves1 = self.pmf_mod_for_sn(self.my_team, False)
        
        moves2 = self.pmf_mod_for_sn(self.op_team, False)
        intersects = self.get_sn_intersection_02(moves1, moves2)

        best_val = 0
        best_move = None
        for i in intersects:
            #print(i)
            if (i[0]['move'].from_value == None):
                calc_val = len(i[0]['between'])   + len(i[1]['behind']) - len(i[1]['between'])
            else:
                calc_val = len(i[0]['between'])+1 + len(i[1]['behind']) - len(i[1]['between'])

            if calc_val > best_val:
                best_val = calc_val
                best_move = i[0]['move']

        return best_move

    # //////////////// subs ////////////////

    def get_sn_intersection_02(self, list1: list[dict], list2: list[dict]) -> list[list[dict, dict]]:

        result = []
        for l1 in list1:
            for l2 in list2:
                if l1['to_value'] == l2['to_value']: result.append([l1, l2])

        return result
        
    # get normalized (direction) vector of vector
    def get_norm_from_vector(self, vector: Vector) -> Vector:

        v_arc = vector.get_arc_tangent()
        v_direction = None
        for direction in Vector().directions:
            if v_arc == direction.get_arc_tangent(): v_direction = direction; break
        return v_direction

    # 'possible moves from', modded for schneider Taktik
    def pmf_mod_for_sn(self, team: Team, one_fish: bool) -> list:

        poss_moves = []
        for p in team.get_penguins():

            for v in Vector().directions:
            
                moves = []
                for i in range(1, self.game_state.board.width()):
                    destination: HexCoordinate = p.coordinate.add_vector(v.scalar_product(i))
                    if self.game_state.board._is_destination_valid(destination):

                        move = Move(team_enum=team.name, from_value=p.coordinate, to_value=destination)
                        vector = Vector(move.to_value.x - move.from_value.x, move.to_value.y - move.from_value.y)

                        full_move = {
                            'move': move,
                            'to_value': move.to_value,
                            'vector': vector,
                            'direction': self.get_norm_from_vector(vector),
                            'between': [],
                            'behind': []
                            }

                        betweens = []
                        for b in moves:
                            betweens.append(b['to_value'])

                        moves.append(full_move)
                    else:
                        break
                
                for a in range(len(moves)):
                    behind = []
                    for b in moves[a + 1:]:
                        behind.append(b['to_value'])
                    moves[a]['behind'] = behind
            
                poss_moves.extend(moves)

        return poss_moves
        
logic = Logic()

if __name__ == "__main__":
    Starter(logic)

