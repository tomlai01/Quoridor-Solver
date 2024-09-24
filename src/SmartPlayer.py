import cProfile

class SmartPlayer:

    def __init__(self, player_id, max_depth):
        self.nodes = dict()
        self.id = player_id
        self.max_depth = max_depth

    def play(self, state):
        """
        play his turn
        :param state: <State> the current state
        :return: <State> the state after his turn
        """
        # pr = cProfile.Profile()
        # pr.enable()
        best_move = None
        best_value = float("inf")
        if state.n == 2:
            root = SmartPlayer.Node(self.id, state)
            for neighbor in root.neighbors():
                move_value = self.alphabeta(neighbor, float("-inf"), float("inf"), self.max_depth)
                if move_value < best_value:
                    best_value = move_value
                    best_move = neighbor.state
            # pr.disable()
            # pr.print_stats(sort='cumtime')
            return best_move

    def alphabeta(self, node, alpha, beta, max_depth, minimize=True):
        if node in self.nodes:
            return self.nodes[node]
        if max_depth == 0 or node.is_leaf() :
            return node.get_value()
        if minimize:  # min node
            value = float("inf")
            for neighbor in node.neighbors():
                value = min(value, self.alphabeta(neighbor, alpha, beta, max_depth - 1, False))
                beta = min(beta, value)
                if value <= alpha:
                    break
            self.nodes[node] = value
            return value
        else:  # max node
            value = float("-inf")
            for neighbor in node.neighbors():
                value = max(value, self.alphabeta(neighbor, alpha, beta, max_depth - 1), True)
                if value >= beta:
                    break
                alpha = max(alpha, value)
            self.nodes[node] = value
            return value
    # ----- Inner Class ---------------------------
    class Node:

        def __init__(self, player_id, state):
            self.id = player_id
            self.other_ids = [o_id for o_id in range(state.n) if o_id != self.id]
            self.state = state
            self.goal = state.goals[player_id]

        def is_leaf(self):
            if self.state.exists_winner() != -1:
                return True
            return False

        def get_value(self):
            if self.state.exists_winner() == self.id:
                return float("-inf")
            elif self.state.exists_winner() in self.other_ids:
                return float("inf")
            # heuristic
            h = abs(self.state.p_positions[self.id][self.goal[0]] - self.goal[1])
            for o_id in self.other_ids:
                o_goal = self.state.goals[o_id]
                h += abs(self.state.p_positions[o_id][o_goal[0]] - o_goal[1])
            return h

        def neighbors(self):
            states = self.state.neighbors()
            return [SmartPlayer.Node(self.id, state) for state in states]

        def __hash__(self):
            return hash(self.state)

        def __eq__(self, other):
            if isinstance(other, SmartPlayer.Node):
                return self.id == other.id and self.state == other.state and self.goal == other.goal
            return False





