from socha import *
import random

class Logic(IClientHandler):

    # //////////////// standard logic ////////////////

    gameState: GameState

    def __init__(self):
        self.my_last_move = None
        self.enemy_copy_rate = []

    def calculate_move(self) -> Move:
        print('\n MY TURN \n')
        self.poss_moves = self.gameState.possible_moves
        self.all_fields = self.gameState.board.get_all_fields()
        self.my_team = self.gameState.current_team
        self.op_team = self.my_team.opponent

        self.my_move = None
        self.rand_move = random.choice(self.poss_moves)

        '''
            PLAN:

            Brücken
            Felderexisting
            Loose parts
            "goldens"
            field score (score via most possible fish on next fields)
            most center: go from center out
            abschneiden (Lucca)
            copy
            copy breaker
        '''

        # if Bot is first:
        if self.my_team == self.gameState.first_team:
            pass
        # if Bot is second:
        else:
            pass

        self.my_move = self.schneider_02()

        # self.my_last_move == None: random, else use:
        self.my_move = self.my_move if self.my_move != None else self.get_least_neighbor_move()
        self.my_last_move = self.my_move
        return self.my_move

    def on_update(self, state: GameState):
        self.gameState = state

    #def while_disconnected(self, player_client):
    #    player_client.connect()
    #    player_client.join_game()

    # //////////////// tactics ////////////////

    def schneider_02(self) -> Move:

        # if first match's turn:
        if self.gameState.turn < 8: 
            moves1 = []
            for p in self.poss_moves:
                moves1.append({
                    'move': p,
                    'to_value': p.to_value,
                    'vector': None,
                    'direction': None,
                    'between': [],
                    'behind': [],
                    'f_score': self.score(p.to_value)
                    })

        else:
            moves1 = self.pmf_mod_for_sn(self.my_team, False)
        
        moves2 = self.pmf_mod_for_sn(self.op_team, False)
        intersects = self.get_sn_intersection_02(moves1, moves2)

        best_val = 0
        best_move = None
        for i in intersects:
            calc_val = 0 \
                + len(i[0]['behind'])   * 0.5 \
                + len(i[0]['between'])  * 1 \
                + i[0]['f_score']       * 0.05 \
                + len(i[1]['behind'])   * 2 \
                - len(i[1]['between'])  * 1.5 \
                
            print(calc_val)

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
                            'behind': [],
                            'f_score': self.score(move.to_value)
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

        '''
        get penguins
        get possible moves from each p 
        -> [Move, to, Vector, direction Vector, list[Field] between from and to, list[Field] after to]
        '''

    def score(self, start: HexCoordinate):

        score = self.gameState.board.get_field(start).fish
        
        for v in Vector().directions:
            for i in range(1, 8):
                destination = start.add_vector(v.scalar_product(i))
                if self.gameState.board._is_destination_valid(destination):
                    score += self.gameState.board.get_field(destination).fish
                else:
                    break

        return score

    def get_least_neighbor_move(logic: 'Logic'):
        min_val = 10
        min_move = logic.gameState.possible_moves[0]

        for move in logic.gameState.possible_moves:
            #state = logic.game_state.perform_move(move)
            valid_n = []
            for each in move.to_value.get_neighbors(): 
                if logic.gameState.board._is_destination_valid(each):
                    valid_n.append(each)
            val = len(valid_n)
            #logging.info(str(val)+ str(valid_n))
            if val <= min_val and not val == 0:
                min_val = val
                min_move = move
        return min_move

    # //////////////// tools ////////////////

    # same function as in socha api, but with possibility for other gamestate than "self.gameState":
    def own_pretty_print(self, gameState: GameState):
        print()
        for i, row in enumerate(gameState.board.board):
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
        
if __name__ == "__main__":
    Starter(Logic())

# NOTIZEN:

# detect brigdes:
# neigbohur fields -> most fields with whitespace

# best score + shortest path if multiple can reach -> else stacking myb
# but if longest path -> can open new possibilities, come out of corners???

# optimize field score: not score all each turn, but edit that ones, that are in line of made move

# optimize field score 2: not score all fields, but only these, where move can be performed from
# bug: recursion does not look at "removed paths"

# optimize field score 3: Whiteboard