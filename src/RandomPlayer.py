import random

class RandomPlayer:

    def __init__(self, player_id):
        self.id = player_id

    def play(self, state):
        """
        play his turn
        :param state: <State> the current state
        :return: <State> the state after his turn
        """
        neighbors = state.neighbors()
        return random.choice(neighbors)