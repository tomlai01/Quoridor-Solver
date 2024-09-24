from src.Exceptions import IllegalPlayException
from src.State import State


class Game:

    def __init__(self, players):
        self.state = State(len(players))
        self.players = players

    def start(self):
        print(f"init game\n{self.state}")
        while self.state.exists_winner() == -1:
            possible_state = set(self.state.neighbors())
            turn = self.state.turn
            next_state = self.players[turn].play(self.state)
            if next_state not in possible_state:
                raise IllegalPlayException(turn)
            self.state = next_state
            print(f"player {turn}:\n{self.state}")
        print(f"The winner is {self.state.exists_winner()}")
