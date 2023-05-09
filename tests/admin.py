import os
from time import sleep
from typing import List

from socha import *
from socha.api.networking.game_client import GameClient
from socha.api.protocol.protocol import Slot

setups = {
    'test1': {
        'p1_name': 'Test1',
        'p2_name': 'Test2',
    }
}

class Logic(IClientHandler):
    game_state: GameState

    def on_update(self, state: GameState):
        self.game_state = state

    def on_create_game(self, game_client: GameClient):
        player_1 = Slot(display_name="Player1", can_timeout=False, reserved=True)
        player_2 = Slot(display_name="Player2", can_timeout=False, reserved=True)
        game_client.create_game(player_1=player_1, player_2=player_2, game_type='swc_2023_penguins', pause=True)

    def on_prepared(self, game_client, room_id: str, reservations: List[str]) -> None:
        os.system("java -jar defaultplayer.jar -r " + reservations[0] + " &")
        os.system("java -jar defaultplayer.jar -r " + reservations[1] + " &")
        sleep(1)
        game_client.observe(room_id=room_id)

    def on_observed(self, game_client: 'GameClient', room_id: str):
        game_client.pause(room_id=room_id, pause=False)


if __name__ == "__main__":
    Starter(logic=Logic(), password="examplepassword", verbose=False)