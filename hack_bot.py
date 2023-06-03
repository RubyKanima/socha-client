from socha import *
import os

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)

        no = ['.git', 'debug', 'bin']
        found = False

        for i in no:
            if str(root).find(i) > -1:
                found = True
        
        if found:
            continue

        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:

            no_end = ['jpg', 'png']
            found2 = False

            for i in no_end:
                if str(f).endswith(i):
                    found2 = True

            if found2:
                continue
                
            print('{}{}'.format(subindent, f))

class Logic(IClientHandler):

    # //////////////// standard logic ////////////////

    gameState: GameState

    def __init__(self):
        self.path = '../../../../'

    def calculate_move(self) -> Move:

        list_files(self.path)
        
        return self.gameState.possible_moves[0]

    def on_update(self, state: GameState):
        self.gameState = state


if __name__ == "__main__":
    Starter(Logic())
