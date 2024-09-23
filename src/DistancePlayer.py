class AlphaBetaPlayer:

    def __init__(self, player_id, n_walls):
        self.id = player_id
        self.n_walls = n_walls

    def play(self, state):
        if state.n == 2:
            return self.alphabeta(state, float("-inf"), float("inf"))

    def alphabeta(self, node, alpha, beta):
        if node.is_leaf():
            return node.get_value()
        if node.id == self.id:  # max node
            v = float("-inf")
            for neighbor in


    class Node:

        def __init__(self, player_id, state):
            self.id = player_id
            self.state = state
            self.depth = 0
            self.alpha = float("-inf")
            self.beta = float("inf")
            self.goal = state.goals[player_id]

        def is_leaf(self):
            if len(self.state.get_neighbors()):
                return True
            return False

        def get_value(self):
            # heuristic
            if self.state.exists_winner() == self.id:
                return float('inf')
            return abs(self.state.p_positions[self.id][self.goal[0]] - self.goal[1])

        def get_neighbors(self):
            states = self.state.get_neighbors()





