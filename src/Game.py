from src.State import State


class Game:

    def __init__(self, players):
        self.state = State(len(players))
        self.players = players

    def start(self):
        while self.state.exists_winner() == -1:
            turn = self.state.turn
            self.state = self.players[turn].play(self.state)
            print(self.state)
        print(f"The winner is {self.state.exists_winner}")
