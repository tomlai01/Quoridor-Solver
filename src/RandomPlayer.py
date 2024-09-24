import random

class RandomPlayer:

    def __init__(self, player_id):
        self.id = player_id

    def play(self, state):
        neighbors = state.neighbors()
        return random.choice(neighbors)