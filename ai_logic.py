from socha import *

import logging
import random
import cProfile
import pstats
import os
import gc

from socha.api.protocol.protocol import Result

from extention import *
from utils import *

collected = gc.collect()

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
    if coordinate == None:
        return None
    return (str(coordinate.x) + str(coordinate.y))

def unhash(hash: str) -> HexCoordinate:
    if hash == None:
        return None
    y = int(hash[-1])
    x = int(hash[0:-1])
    return HexCoordinate(x, y)

def move_from_hashes(f_hash: str, t_hash: str, team: TeamEnum) -> Move:
    return Move(team_enum=team, from_value=unhash(f_hash), to_value=unhash(t_hash))

class Logic(IClientHandler):
    def __init__(self):     
        self.game_state: GameState
        self.tri_board: TriBoard
        self.team = False

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
        
        if(not self.team): #get own team
            self.team = self.game_state.current_team

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
            
            if move.from_value != None:
                f_tile = self.tri_board.get_tile(move.from_value)
                f_hash = hash(f_tile.root)
            else:
                f_tile = None
                f_hash = None

            t_tile = self.tri_board.get_tile(move.to_value)
            t_hash = hash(t_tile.root)


            has_e_int = True if t_hash in inters_from_own else False

            ai_info = {
                "f_hash": f_hash,
                "t_hash": t_hash,

                "w": 0,                                                                                             # white 0 / 1
                "r": 0,                                                                                             # red 0 / 1
                "b": 0,                                                                                             # black 0 / 1
                "y": 0,                                                                                             # yellow (dead end) 0 / 1

                "fish": t_tile.fish,                                                                                # fish 1 - 4
                "fish_m": linear_map(0, 4, t_tile.fish),                                                            # fish mapped 0 - 1    
                "fish_gr": self.tri_board.groups[t_tile.group].fish,                                                # fish group 1 - x 
                "fish_gr_p": round(self.tri_board.groups[t_tile.group].fish / all_fish, 3),                         # fish group percent 0 - 1
                "fish_po": self.tri_board.get_possible_fish(t_tile.root),                                           # fish possible 1 - x

                "tri_int": t_tile.inters,                                                                           # triangle intersections 0 - 6
                "tri_int_m": linear_map(0, 6, t_tile.inters),                                                       # triangle intersections mapped 0 - 1

                "e_int": inters_from_own[t_hash]["count"] if has_e_int else 0,                                      # intersections with enemy 0 - 9
                "e_int_m": round(linear_map(0, 9, inters_from_own[t_hash]["count"], 3) if has_e_int else 0),        # intersections with enemy mapped 0 - 1
                "e_int_beh": inters_from_op[t_hash]["behind"] if has_e_int else 0,                                  # behind enemy pov 0 - x
                "e_int_bet": inters_from_op[t_hash]["between"] if has_e_int else 0,                                 # between enemy pov 0 - x
                "e_int_o_beh": inters_from_own[t_hash]["behind"] if has_e_int else 0,                               # behind AI pov 0 - x
                "e_int_o_bet": inters_from_own[t_hash]["between"] if has_e_int else 0,                              # between AI pov 0 - x

                #"mate_inters": 0,
                #"mate_inters_mapped": 0,
                #"mate_behinds": 0,
                #"mate_between": 0,
                #"mate_own_behind": 0,
                #"mate_own_between": 0,
            }

            """
            notes:

            go through every poss move
            instead of between and behind -> poss moves if move made
            """

            ai_info[t_tile.spot[0]] = 1

            ai_infos.append(ai_info)



            # ai for each field here
            # evaluate best field




        #tabulate_ai_infos(ai_infos)

        # AI calculates move
        global net, wanted_keys

        ai_infos_array = ai_infos_converter(ai_infos, wanted_keys)

        result = net.calculateMove(ai_infos_array)
        
        return self.game_state.possible_moves[result]
    
    def on_game_over(self, roomMessage: Result) -> None:

        print("[game ended]")
        
        global games_won, games_played, learn, net
        
        games_played += 1

        if ((not roomMessage.winner is None) and (self.team.name.name == roomMessage.winner.team)): 
            print("You won, Player {0}".format(self.team.name.name))
            
            log = "WIN"
            
            games_won += 1
            evaluation = max(roomMessage.scores.entry[0].score.part[1], roomMessage.scores.entry[1].score.part[1]) - min(roomMessage.scores.entry[0].score.part[1], roomMessage.scores.entry[1].score.part[1])
        else:
            print("u stupid bro", self.team.name.name)
            
            log = "LOSS"
            evaluation = min(roomMessage.scores.entry[0].score.part[1], roomMessage.scores.entry[1].score.part[1]) - max(roomMessage.scores.entry[0].score.part[1], roomMessage.scores.entry[1].score.part[1])

        log += " ME:" + self.team.name.name
        log += " ONE: " + str(roomMessage.scores.entry[0].score.part[0]) + " " + str(roomMessage.scores.entry[0].score.part[1])
        log += " TWO: " + str(roomMessage.scores.entry[1].score.part[0]) + " " + str(roomMessage.scores.entry[1].score.part[1])
        log += " RM: " + str(roomMessage.scores.entry[0].player.name)

        save_log(log)

        if(learn):
            net.update_prep(evaluation)
            
        self.team = False

        global games_won_all, moves_made, moves_made_all

        if ((games_played) % learning_interval == 0): #its learnin time
            ask_to_save(net, "Loop_" + str((games_played + 1)))

            log = "{0} loops complete, {1}/{2} games won".format((games_played), games_won, learning_interval)

            save_log(log)
            

            print("[now evaluating]")

            net.update(eta= 0.1, amount= learning_interval)
            

            games_won_all += games_won
            games_won = 0

            moves_made_all += moves_made
            moves_made = 0

        
        #clearing shit
        self.history.clear()
        #os.system('cls')

        return super().on_game_over(roomMessage)

games_won = 0
games_won_all = 0

moves_made = 0
moves_made_all = 0

games_played = 0

wanted_keys = ["w", "r", "b", "y", "fish_m", "fish_gr_p", "tri_int_m", "e_int_m", "e_int_beh", "e_int_bet", "e_int_o_beh", "e_int_o_bet"]

print("Neurons needed in first layer: {0}".format(len(wanted_keys)))

sizes, file = get_network()

net = network(sizes= sizes, file= file)

if __name__ == "__main__":

    learn = (input("Should the AI learn(y/n): ") == "y")
    learning_interval = int(input("What should the logging and learning interval be(int): "))

    test = Starter(logic=Logic(), survive= True, auto_reconnect= True)