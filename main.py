from src.Game import Game
from src.RandomPlayer import RandomPlayer
from src.SmartPlayer import SmartPlayer

if __name__ == '__main__':
    game = Game([RandomPlayer(0), SmartPlayer(1, 1)])
    game.start()


