from socha import *
import logging
import random

class Logic(IClientHandler):

    game_state: GameState

    def __init__(self):
        self.enemy_copy_rate = []

    def on_update(self, state: GameState):
        self.game_state = state

    def calculate_move(self) -> Move:
        
        self.all_fields = self.game_state.board.get_all_fields()
        self.my_team: Team = self.game_state.current_team
        self.op_team: Team =  self.game_state.current_team.opponent
        self.poss_moves = self.game_state.possible_moves
        self.other_poss_moves = self.game_state._get_possible_moves(self.op_team)
        self.inner_join = [[each, other] for each in self.poss_moves for other in self.other_poss_moves if each.to_value == other.to_value]
        self.rand_move = random.choice(self.poss_moves)
        if self.game_state.turn < 8:
            #return self.best_possible_field()
            return self.rand_move
        self.my_move: Move = None
        if not self.other_poss_moves:
            return self.get_depth_move()
        if not self.inner_join:
            return self.max_move()
        return self.intersect_move()

    def intersect_move(self):
        logging.info("INTERSECT")
        if self.game_state.turn < 8: 
            moves1 = []
            for p in self.poss_moves:
                moves1.append([p, p.to_value, None, None, [], []])
            logging.info("turn < 8")
        else:
            moves1 = self.intersections_info_list(self.my_team, False)
        moves2 = self.intersections_info_list(self.op_team, False)
        intersects = self.get_intersections(moves1, moves2)
        best_val = 0
        best_move = self.rand_move
        #logging.info(f" \n Moves1: \n {moves1} \n Moves2: \n {moves2} \n Intersects: \n {intersects}")
        for each in intersects:
            val = self.intersect_evaluate(each)
            if val > best_val:
                best_move = each[0][0]
                best_val = val
        return best_move
    
    def intersect_evaluate(self, intersection) -> Move:
        turn_add = 1 if self.game_state.turn <= 8 else 0
        return len(intersection[0][4]) + turn_add  + len(intersection[1][5]) - len(intersection[1][4]) 
                
    def get_intersections(self, list1: list[list], list2: list[list]) -> list[list[list, list]]:
        result = []
        for l1 in list1:
            for l2 in list2:
                if l1[1] == l2[1]: result.append([l1, l2])
        return result
        
    def get_norm_from_vector(self, vector: Vector) -> Vector:
        arc = vector.get_arc_tangent()
        direction = None
        for xdir in Vector().directions:
            direction = xdir if arc == xdir.get_arc_tangent() else direction
        return direction

    def intersections_info_list(self, team: Team, one_fish: bool) -> list:
        poss_moves = []
        for p in team.get_penguins():
            for v in Vector().directions:
                moves = []
                for i in range(1, self.game_state.board.width()):                                              
                    destination : HexCoordinate = p.coordinate.add_vector(v.scalar_product(i))                   
                    if self.game_state.board._is_destination_valid(destination):                          
                        move = Move(team_enum=team.name, from_value = p.coordinate, to_value=destination)        
                        vector = Vector(move.to_value.x - move.from_value.x, move.to_value.y - move.from_value.y)   
                        direction = self.get_norm_from_vector(vector)                                             
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
    
    def own_pretty_print(self, game_state: GameState):
        print()
        for i, row in enumerate(game_state.board.board):
            if (i + 1) % 2 == 0:
                print(" ", end="")
            for field in row:
                if field.is_empty():
                    print("~", end=" ")
                elif field.is_occupied():
                    print(field.get_team().value[0], end=" ")
                else:
                    print(field.get_fish(), end=" ")
            print()
        print()
        
    #alpha beta

    def move_hash(self, state: GameState):
        move_list = []
        for move in state.first_team.moves:
            move_str = str(move.to_value.x)+str(move.to_value.y)+str(move.team_enum.name)
            move_list.append(move_str)
        for move in state.second_team.moves:
            move_str = str(move.to_value.x)+str(move.to_value.y)+str(move.team_enum.name)
            move_list.append(move_str)
        return str(set(move_list))

    def alpha_beta(self, new_state: GameState, depth: int, alpha, beta, memo : dict = {}):
            logging.info("ALPHA BETA")
            hash_list = self.move_hash(new_state)
            value = self.fish_evaluate(new_state)
            if hash_list in memo:
                return memo[hash_list]
            if depth == 0 or new_state.current_team == None:
                return value #  value berechnen
            maximizing = (new_state.current_team.name == self.game_state.current_team.name)
            if maximizing:
                if new_state.possible_moves == []:
                    return value
                maxEval = -100 # replacement (- inf)
                for child in new_state.possible_moves:
                    eval = self.alpha_beta(new_state.perform_move(child), depth - 1, alpha, beta, memo)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                memo[hash_list] = maxEval
                return maxEval

            else:
                minEval = 100 # replacement (- inf)
                for child in new_state.possible_moves:
                    eval = self.alpha_beta(new_state.perform_move(child), depth - 1, alpha, beta, memo)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                memo[hash_list] = minEval
                return minEval
            
    def max_move(self):
        max_move = None
        max_val = -1000
        # actual alpha_beta:
        for child in self.game_state.possible_moves:
            if len(self.game_state.board.get_empty_fields()) > 50:
                mini_max = self.alpha_beta(self.game_state.perform_move(child), 2, max_val, 100)
            else:
                mini_max = self.alpha_beta(self.game_state.perform_move(child), 1, max_val, 100)
            val = mini_max
            if val > max_val:
                max_move = child
                max_val = val
        return max_move

    def fish_evaluate(self, state: GameState) -> int:
        if (self.game_state.current_team.name == self.game_state.first_team.name):
            max = state.first_team.fish
            min = state.second_team.fish
        else:
            min = state.first_team.fish
            max = state.second_team.fish
        return max - min

    def get_depth_move(self):
        best_move: Move = None
        best_val: int = 0
        for each in self.poss_moves:
            val = self._depth_search(self.game_state.perform_move(each), 1)
            if val > best_val:
                best_val = val
                best_move = each
        return best_move

    def depth_search(self, new_state: GameState, depth: int):
        maximizing = (new_state.current_team.name == self.game_state.current_team.name)
        if new_state.current_team == None:
            return depth
        if maximizing:
            if new_state.possible_moves == []:
                    return depth
            for each in new_state.possible_moves:
                return self.depth_search(new_state.perform_move(each), depth+1)
        else:
            for each in new_state.possible_moves:
                return self.depth_search(new_state.perform_move(each), depth)
    
    def _depth_search(self, new_state: GameState, depth: int):
        if new_state.current_team == None or new_state.possible_moves == []:
            return depth
        for each in new_state.possible_moves:
                return self._depth_search(new_state.perform_move(each), depth+1)
     
if __name__ == "__main__":
    Starter(Logic())