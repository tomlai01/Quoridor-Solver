class SmartPlayer:

    def __init__(self, player_id):
        self.id = player_id
        self.nodes = dict()

    def play(self, state):
        if state.n == 2:
            root = SmartPlayer.Node(self.id, state)
            best_value = self.alphabeta(root, float("-inf"), float("inf"), 2)
            for neighbor in root.neighbors():
                if self.nodes[neighbor] == best_value:
                    return neighbor.state

    def alphabeta(self, node, alpha, beta, depth):
        if node in self.nodes.keys():
            return self.nodes[node]
        if node.is_leaf() or depth == 0:
            v = node.get_value()
            self.nodes[node] = v
            return v
        if node.id == self.id:  # max node
            v = float("-inf")
            for neighbor in node.neighbors():
                v = max(v, self.alphabeta(neighbor, alpha, beta, depth-1))
                if v >= beta:
                    break
                alpha = max(alpha, v)
            self.nodes[node] = v
            return v
        else:  # min node
            v = float("inf")
            for neighbor in node.neighbors():
                v = min(v, self.alphabeta(neighbor, alpha, beta, depth-1))
                if v <= beta:
                    break
                beta = min(beta, v)
            self.nodes[node] = v
            return v

    class Node:

        def __init__(self, player_id, state):
            self.id = player_id
            self.state = state
            self.depth = 0
            self.alpha = float("-inf")
            self.beta = float("inf")
            self.goal = state.goals[player_id]

        def is_leaf(self):
            if len(self.state.get_neighbors()) == 0:
                return True
            return False

        def get_value(self):
            # heuristic
            if self.state.exists_winner() == self.id:
                return float('inf')
            return abs(self.state.p_positions[self.id][self.goal[0]] - self.goal[1])

        def neighbors(self):
            states = self.state.get_neighbors()
            return [SmartPlayer.Node(state.turn, state) for state in states]





