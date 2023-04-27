from socha import *
from logic import Logic
import logging

class Intersection():

    def __init__(self, game_state, move):
        self.move: Move
        self.vector: Vector
        self.betweens: int = self._get_betweens()
        self.after: int = self._get_after()

    def _get_betweens():
        '''missing code'''

    def _get_after():
        '''missing code'''

    def intersect_move(logic: Logic):
        if logic.game_state.turn < 8: 
            moves1 = []
            for p in logic.game_state.possible_moves:
                moves1.append([p, p.to_value, None, None, [], []])
            logging.info("turn < 8")
        else:
            moves1 = Intersection.intersections_info_list(logic.game_state.current_team, False)
        moves2 = Intersection.intersections_info_list(logic.game_state.other_team, False)
        intersects = Intersection.get_intersections(moves1, moves2)
        best_val = 0
        best_move = None
        for each in intersects:
            val = Intersection.intersect_evaluate(each)
            if val > best_val:
                best_move = each[0][0]
                best_val = val
        return best_move
    
    def intersect_evaluate(logic: Logic, intersection) -> Move:
        turn_add = 1 if logic.game_state.turn <= 8 else 0
        return len(intersection[0][4]) + turn_add  + len(intersection[1][5]) - len(intersection[1][4]) 
                
    def get_intersections(logic, list1: list[list], list2: list[list]) -> list[list[list, list]]:
        result = []
        for l1 in list1:
            for l2 in list2:
                if l1[1] == l2[1]: result.append([l1, l2])
        return result
        
    def get_norm_from_vector(logic, vector: Vector) -> Vector:
        arc = vector.get_arc_tangent()
        direction = None
        for xdir in Vector().directions:
            direction = xdir if arc == xdir.get_arc_tangent() else direction
        return direction

    def intersections_info_list(logic: Logic, team: Team) -> list:
        '''
        `intersections_info_list` returns a list of info:
            - [0]: `Move`
            - [1]: `destination` / `to_value` 
            - [2]: `vector`
            - [3]: `direction`
            - [4]: `betweens`
        '''
        poss_moves = []
        for p in team.get_penguins():
            for v in Vector().directions:
                moves:list = []
                for i in range(1, logic.game_state.board.width()):                                              
                    destination : HexCoordinate = p.coordinate.add_vector(v.scalar_product(i))                   
                    if logic.game_state.board._is_destination_valid(destination):                          
                        move = Move(team_enum=team.name, from_value = p.coordinate, to_value=destination)        
                        vector = Vector(move.to_value.x - move.from_value.x, move.to_value.y - move.from_value.y)   
                        direction = Intersect.get_norm_from_vector(vector)                                             
                        betweens = []
                        for b in moves:                                                                             
                            betweens.append(b[1])
                        moves.append([move, destination, vector, direction, betweens])
                    else:   # If out of bounds
                        break
                
                for a in range(len(moves)):
                    afters = []
                    for b in moves[a + 1:]:
                        afters.append(b[1])
                    moves[a].append(afters)
            
                poss_moves.extend(moves)
                #logging.info(poss_moves)
        return poss_moves
    
    def pmf_mod_for_sn(self, team: Team, one_fish: bool) -> list:

        poss_moves = []
        for p in team.get_penguins():

            for v in Vector().directions:
            
                moves = []
                for i in range(1, self.gameState.board.width()):
                    destination: HexCoordinate = p.coordinate.add_vector(v.scalar_product(i))
                    if self.gameState.board._is_destination_valid(destination):

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