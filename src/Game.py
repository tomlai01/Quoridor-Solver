from State import State


class Game:

    def __init__(self, players):
        self.state = State(len(players))
        self.players = players

    def play(self):
        turn = self.state.turn
        self.state = self.players[turn].play(self.state)
