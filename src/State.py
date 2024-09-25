from copy import deepcopy
from queue import PriorityQueue
from heapdict import heapdict

class State:

    def __init__(self, n):
        """
        :param n: <int> players number
        """
        self.n = n  # players number
        self.turn = 0  # player's turn
        self.h_walls = set()  # horizontal walls position as (i, j) corresponding to the square at the top left of the wall
        self.v_walls = set()  # vertical walls position as (i, j) corresponding to the square at the top left of the wall

        if n not in [2, 4]:  # Handle players number error
            raise ValueError("The players number must be 2 or 4")
        if n == 2:  # two players
            self.p_positions = [(0,4), (8,4)]  # players position
            self.goals = [(0,8), (0,0)]  # (index, position) example: player 1 has to reach the line i = 8 then goals[0] = (0, 8), player 3 has to reach the line j = 0 then goals[2] = (1, 0)
            self.walls = [10, 10]  # number of walls for each player
        if n == 4:  # four players
            self.p_positions = [(0, 4), (8, 4), (4, 0), (4, 8)]
            self.goals = [(0, 8), (0, 0), (1, 8), (1, 0)]
            self.walls = [5, 5, 5, 5]

    def exists_winner(self):
        """
        check if there is a winner and return it in that case
        :return: <int> the id of the winning player or -1 if no winner yet
        """
        if self.p_positions[0][0] == 8:  # player 1 has won
            self.winner = 0
            return 0
        elif self.p_positions[1][0] == 0:  # player 2 has won
            self.winner = 1
            return 1
        if self.n == 4:
            if self.p_positions[2][1] == 8:  # player 3 has won
                self.winner = 2
                return 2
            elif self.p_positions[3][1] == 0:  # player 4 has won
                self.winner = 3
                return 3
        return -1

    def through_wall(self, from_position, to_position):
        """
        check if going from from_position to to_position through a wall
        :param from_position: <(int, int)> the start position as (i, j)
        :param to_position: <(int, int)> the end position as (i, j)
        :return: <boolean> goes through the wall
        """
        if to_position[0] < from_position[0]:  # go to the north
            if to_position in self.h_walls or (to_position[0], to_position[1] - 1) in self.h_walls:  # north wall ?
                return True
        elif to_position[1] > from_position[1]:  # go to the east
            if from_position in self.v_walls or (from_position[0] - 1, from_position[1]) in self.v_walls:  # east wall ?
                return True
        elif to_position[0] > from_position[0]:  # go to the south
            if from_position in self.h_walls or (from_position[0], from_position[1] - 1) in self.h_walls:  # south wall ?
                return True
        elif to_position[1] < from_position[1]:  # go to the west
            if to_position in self.v_walls or (to_position[0] - 1, to_position[1]) in self.v_walls:  # west wall ?
                return True
        else:
            raise RuntimeError()
        return False

    def can_move(self, from_position, to_position):
        """
        Check if the player can move to the from_position without taking into account other players
        :param from_position: <(int, int)> the position the player wants to move from
        :param to_position: <(int, int)> the position the player wants to move to
        :return: <boolean> the player can move to the from_position
        """
        # assert not move in diagonal
        if from_position[0] != to_position[0]:
            assert from_position[1] == to_position[1]
        # assert move to an adjacent square
        assert -1 <= from_position[0] - to_position[0] <= 1
        assert -1 <= from_position[1] - to_position[1] <= 1

        if 0 <= from_position[0] <= 8 and 0 <= from_position[1] <= 8 and 0 <= to_position[0] <= 8 and 0 <= to_position[1] <= 8:  # check in board
            if not self.through_wall(from_position, to_position):  # check if move through a wall
                return True
        return False

    def check_solution(self, solution):
        for i in range(len(solution)-1):
            if not self.can_move(solution[i], solution[i+1]):
                return False
        return True

    def exists_solution(self, previous_solutions):
        """
        check each player can reach his goal
        :return: <boolean> each player can reach his goal
        """
        for i in range(self.n):
            if len(previous_solutions[i]) > 0 and self.check_solution(previous_solutions[i]):
                continue
            else:
                solution = self.best_first_search(self.p_positions[i], self.goals[i])
                if len(solution) < 0:
                    return False
                previous_solutions[i] = solution
        return True

    def best_first_search(self, start, goal):
        """
        find the shortest path from start to goal
        :param start: <(int, int)> the start position
        :param goal: <(int, int)> (index, position) example: player 1 has to reach the line i = 8 then goals[0] = (0, 8), player 3 has to reach the line j = 0 then goals[2] = (1, 0)
        :return: <boolean> it exists a path from start to goal
        """
        # ----- Inner functions -------------------------
        def neighbors():
            neighbors = []
            if self.can_move(position, (position[0]-1, position[1])):
                neighbors.append((position[0]-1, position[1]))
            if self.can_move(position, (position[0], position[1]+1)):
                neighbors.append((position[0], position[1]+1))
            if self.can_move(position, (position[0]+1, position[1])):
                neighbors.append((position[0]+1, position[1]))
            if self.can_move(position, (position[0], position[1]-1)):
                neighbors.append((position[0], position[1]-1))
            return neighbors
        # ----------------------------------------------
        came_from = {}
        visited = set()
        queue = PriorityQueue()
        queue.put((abs(goal[1] - start[goal[0]]), start))
        while not queue.empty():
            priority, position = queue.get()
            for neighbor in neighbors():
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = position
                    if neighbor[goal[0]] == goal[1]:
                        path = []
                        while neighbor != start:
                            path.append(neighbor)
                            neighbor = came_from[neighbor]
                        path.append(start)
                        return path[::-1]
                    queue.put((abs(goal[1] - neighbor[goal[0]]), neighbor))
        return []

    def can_place(self, is_horizontal, position, previous_solutions):
        """
        check if the wall can be placed at the given position
        :param is_horizontal: <boolean> if wall to place is horizontal or vertical
        :param position: <(int, int)> position of the wall as (i, j) corresponding to the square top left of the wall
        :return: <boolean> if the wall can be placed at the given position
        """
        assert 0 <= position[0] <= 7 and 0 <= position[1] <= 7  # assert in board
        if is_horizontal:
            if position in self.h_walls or (position[0], position[1]-1) in self.h_walls \
                    or (position[0], position[1]+1) in self.h_walls or position in self.v_walls:
                return False
            self.h_walls.add(position)
            if not self.exists_solution(previous_solutions):
                self.h_walls.remove(position)
                return False
            self.h_walls.remove(position)
        else:
            if position in self.v_walls or (position[0]-1, position[1]) in self.v_walls \
                    or (position[0]+1, position[1]) in self.v_walls or position in self.h_walls:
                return False
            self.v_walls.add(position)
            if not self.exists_solution(previous_solutions):
                self.v_walls.remove(position)
                return False
            self.v_walls.remove(position)
        return True

    def neighbors(self):
        """
        :return: <list<State>> list of possible neighbors
        """
        # ----- Inner functions -------------------------
        def facing(current_position, concurrent_position, facing_position):
            """
            Handle facing move
            :param current_position: <(int, int)> player current position
            :param concurrent_position: <(int, int)> position where the other player is
            :param facing_position: <(int, int)> position where the player should go if he jumps over the other player going straight
            """
            if self.can_move(concurrent_position, facing_position):  # can just jump over the other
                copy = deepcopy(self)
                copy.p_positions[self.turn] = facing_position
                copy.turn = (self.turn + 1) % self.n
                neighbors.append(copy)
            else:  # try to jump in diagonal
                moves = [(-1, 0), (0, -1), (0, 1), (1, 0)]
                for move in moves:
                    new_position = (concurrent_position[0] + move[0], concurrent_position[1] + move[1])
                    if new_position != current_position and new_position != facing_position and self.can_move(concurrent_position, new_position):
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = new_position
                        copy.turn = (self.turn + 1) % self.n
                        neighbors.append(copy)
        # ---------------------------------------------
        neighbors = []
        current_position = self.p_positions[self.turn]
        other_positions = [self.p_positions[p_id] for p_id in [i for i in range(self.n)] if p_id != self.turn]  # other players' positions
        # moving
        moves = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for move in moves:
            new_position = current_position[0] + move[0], current_position[1] + move[1]
            if self.can_move(current_position, new_position):
                if new_position in other_positions:
                    facing_position = new_position[0] + move[0], new_position[1] + move[1]
                    facing(current_position, new_position, facing_position)
                else:
                    copy = deepcopy(self)
                    copy.p_positions[self.turn] = (new_position)
                    copy.turn = (self.turn + 1) % self.n
                    neighbors.append(copy)
        # placing wall
        previous_solutions = {i:[] for i in range(self.n)}
        if self.walls[self.turn] > 0:  # check if player has any walls left
            # try to place a horizontal wall
            for i in range(8):
                for j in range(8):
                    if self.can_place(True, (i, j), previous_solutions):
                        copy = deepcopy(self)
                        copy.h_walls.add((i, j))
                        copy.walls[self.turn] -= 1
                        copy.turn = (self.turn + 1) % self.n
                        neighbors.append(copy)
            # try to place a vertical wall
            for i in range(8):
                for j in range(8):
                    if self.can_place(False, (i, j), previous_solutions):
                        copy = deepcopy(self)
                        copy.v_walls.add((i, j))
                        copy.walls[self.turn] -= 1
                        copy.turn = (self.turn + 1) % self.n
                        neighbors.append(copy)
        return neighbors

    def __hash__(self):
        return hash((tuple(self.p_positions), frozenset(self.h_walls), frozenset(self.v_walls), self.turn))

    def __eq__(self, other):
        if isinstance(other, State):
            return self.n == other.n and self.turn == other.turn and self.h_walls == other.h_walls \
                    and self.v_walls == other.v_walls and self.p_positions == other.p_positions \
                    and self.walls == other.walls and self.goals == other.goals
        return False

    def __str__(self):
        s = f"players' position: p.0: {self.p_positions[0]}, p.1: {self.p_positions[1]}\n" \
            f"horizontal walls: {self.h_walls}\n" \
            f"vertical walls: {self.v_walls}\n"
        return s
