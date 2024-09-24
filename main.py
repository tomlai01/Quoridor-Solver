from src.Game import Game
from src.RandomPlayer import RandomPlayer
from src.SmartPlayer import SmartPlayer

if __name__ == '__main__':
    game = Game([SmartPlayer(1, 1), SmartPlayer(1, 2)])
    game.start()


