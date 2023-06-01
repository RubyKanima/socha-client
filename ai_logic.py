from socha import *

import logging
import random

from extention import *
from utils import *


def inters_for_ai(state: GameState, team: TeamEnum, op_team: TeamEnum) -> list[dict]:
    
    pm_from_peng_op = get_possible_fields(state, op_team)

    intersections = {}
    for p in state.board.get_teams_penguins(team):
        for v in Vector().directions:
            inters_for_dir = {}
            for i in range(1, 8):
                destination: HexCoordinate = p.coordinate.add_vector(v.scalar_product(i))
                if own_is_valid(destination) and state.board.get_field(destination).fish > 0:
                    
                    for inter in inters_for_dir:
                        inters_for_dir[inter]["behind"] += 1 * inters_for_dir[inter]["count"]

                    count = pm_from_peng_op.count(state.board.get_field(destination))
                    if count > 0:
                        inters_for_dir[hash(destination)] = {"between": (i - 1) * count, "behind": 0, "count": count}
                else:
                    break
                
            # add inters_for_dir to intersections
                    
            for inter in inters_for_dir:
                if inter in intersections:
                    intersections[inter]["between"] += inters_for_dir[inter]["between"]
                    intersections[inter]["behind"] += inters_for_dir[inter]["behind"]
                    intersections[inter]["count"] += inters_for_dir[inter]["count"]
                else:
                    intersections[inter] = inters_for_dir[inter]
            
            

    return intersections

def hash(coordinate: HexCoordinate):
    return (str(coordinate.x) + str(coordinate.y))


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


        # yes

        # all fish from all groups
        all_fish = 0
        for g in self.tri_board._groups:
            all_fish += g.fish

        # inters
        inters_from_own = inters_for_ai(self.game_state, self.game_state.current_team.name, self.game_state.current_team.opponent.name)
        inters_from_op = inters_for_ai(self.game_state, self.game_state.current_team.opponent.name, self.game_state.current_team.name)     
                
        ai_infos = []
        
        # make ai dict
        for move in self.game_state.possible_moves:
            
            tile = self.tri_board.get_tile(move.to_value)
            _hash = hash(tile.root)
            
            has_e_int = True if _hash in inters_from_own else False

            ai_info = {
                "hash": _hash,
                          
                "white": 0,
                "red": 0,
                "black": 0,
                "yellow": 0,

                "fish": tile.fish,
                "fish_mapped": linear_map(0, 4, tile.fish),
                "fish_group": self.tri_board.groups[tile.group].fish, # value
                "fish_group_percent": round(self.tri_board.groups[tile.group].fish / all_fish, 3), # percent of board
                "fish_possible": self.tri_board.get_possible_fish(tile.root),

                "tri_inters": tile.inters,
                "tri_inters_mapped": linear_map(1, 6, tile.inters),

                "e_int": inters_from_own[_hash]["count"] if has_e_int else 0,
                "e_int_mapped": round(linear_map(0, 9, inters_from_own[_hash]["count"], 3) if has_e_int else 0),
                "e_int_behinds": inters_from_op[_hash]["behind"] if has_e_int else 0,
                "e_int_between": inters_from_op[_hash]["between"] if has_e_int else 0,
                "e_int_own_behind": inters_from_own[_hash]["behind"] if has_e_int else 0,
                "e_int_own_between": inters_from_own[_hash]["between"] if has_e_int else 0,

                #"mate_inters": 0,
                #"mate_inters_mapped": 0,
                #"mate_behinds": 0,
                #"mate_between": 0,
                #"mate_own_behind": 0,
                #"mate_own_between": 0,
            }

            ai_info[tile.spot] = 1

            ai_infos.append(ai_info)

            # ai for each field here
            # evaluate best field
        tabulate_ai_infos(ai_infos)
        # take best here
        # and eval your neural network
        
        return random.choice(self.game_state.possible_moves)
        
if __name__ == "__main__":
    Starter(Logic())