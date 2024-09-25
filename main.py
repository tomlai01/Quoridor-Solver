from src.Game import Game
from src.RandomPlayer import RandomPlayer
from src.SmartPlayer import SmartPlayer

if __name__ == '__main__':
    game = Game([SmartPlayer(0, 3), SmartPlayer(1, 3)])
    game.start()


