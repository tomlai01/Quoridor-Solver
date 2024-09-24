from copy import deepcopy
from queue import PriorityQueue

import numpy as np

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
        :return: <int> the id of the winning player or -1 if no winner yet
        """
        if self.p_positions[0][0] == 8:  # player 1 has won
            return 0
        elif self.p_positions[1][0] == 0:  # player 2 has won
            return 1
        if self.n == 4:
            if self.p_positions[2][1] == 8:  # player 3 has won
                return 2
            elif self.p_positions[3][1] == 0:  # player 4 has won
                return 3
        return -1

    def can_move(self, from_p, to_p):
        """
        Check if the player can move to the from_p without taking into account other players
        :param from_p: <tuple> the position the player wants to move from
        :param to_p: <tuple> the position the player wants to move to
        :return: <boolean> the player can move to the from_p
        """
        # assert not move in diagonal
        if from_p[0] != to_p[0]:
            assert from_p[1] == to_p[1]
        # assert move to an adjacent square
        assert -1 <= from_p[0] - to_p[0] <= 1
        assert -1 <= from_p[1] - to_p[1] <= 1

        if 0 <= from_p[0] <= 8 and 0 <= from_p[1] <= 8 and 0 <= to_p[0] <= 8 and 0 <= to_p[1] <= 8:  # check in board
            if to_p[0] < from_p[0]:  # go to the north
                if to_p not in self.h_walls and (to_p[0], to_p[1]-1) not in self.h_walls:  # no north wall ?
                    return True
            if to_p[1] > from_p[1]:  # go to the east
                if from_p not in self.v_walls and (from_p[0]-1, from_p[1]) not in self.v_walls:  # no east wall ?
                    return True
            if to_p[0] > from_p[0]:  # go to the south
                if from_p not in self.h_walls and (from_p[0], from_p[1]-1) not in self.h_walls:  # no south wall ?
                    return True
            if to_p[1] < from_p[1]:  # go to the west
                if to_p not in self.v_walls and (to_p[0]-1, to_p[1]) not in self.v_walls:  # no west wall ?
                    return True
        return False

    def exists_solution(self):
        """
        :return: <boolean> each player can reach his goal
        """
        for i in range(self.n):
            if not self.best_first_search(self.p_positions[i], self.goals[i]):
                return False
        return True

    def best_first_search(self, start, goal):
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
        visited = set()
        queue = PriorityQueue()
        queue.put((abs(goal[1] - start[goal[0]]), start))
        while not queue.empty():
            priority, position = queue.get()
            for neighbor in neighbors():
                if neighbor not in visited:
                    if neighbor[goal[0]] == goal[1]:
                        return True
                    visited.add(neighbor)
                    queue.put((abs(goal[1] - neighbor[goal[0]]), neighbor))
        return False

    def can_place(self, is_horizontal, position):
        """
        :param is_horizontal: <boolean> if wall to place is horizontal or vertical
        :param position: <tuple> position of the wall as (i, j) corresponding to the square top left of the wall
        :return: <boolean> if the wall can be placed at the given position
        """
        assert 0 <= position[0] <= 7 and 0 <= position[1] <= 7  # assert in board
        if is_horizontal:
            if position in self.h_walls or (position[0], position[1]-1) in self.h_walls \
                    or (position[0], position[1]+1) in self.h_walls or position in self.v_walls:
                return False
            self.h_walls.add(position)
            if not self.exists_solution():
                self.h_walls.remove(position)
                return False
            self.h_walls.remove(position)
        else:
            if position in self.v_walls or (position[0]-1, position[1]) in self.v_walls \
                    or (position[0]+1, position[1]) in self.v_walls or position in self.h_walls:
                return False
            self.v_walls.add(position)
            if not self.exists_solution():
                self.v_walls.remove(position)
                return False
            self.v_walls.remove(position)
        return True


    def get_neighbors(self):
        """
        :return: <list<State>> list of possible neighbors
        """
        # ----- Inner functions -------------------------
        def next_turn(state):
            """
            Pass the state to next round
            :param state: (State)
            :return: (State) state with the turn passes to the next player
            """
            if state.turn < state.n - 1:
                state.turn += 1
            else:
                state.turn = 0
            return state            

        def facing(facing_position):
            """
            Handle facing move
            :param facing_position: <(int, int)>
            """
            if facing_position[0] < current_position[0]:  # check if come from south
                if self.can_move(facing_position, (facing_position[0]-1, facing_position[1])):  # can go to the north ?
                    if (facing_position[0]-1, facing_position[1]) not in other_positions:  # not arrived on another player
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0] - 1, facing_position[1])
                        copy = next_turn(copy)
                        neighbors.append(copy)
                else:
                    if self.can_move(facing_position, (facing_position[0], facing_position[1] - 1)) \
                            and (facing_position[0], facing_position[1] - 1) not in other_positions:  # can go to the west ?
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0], facing_position[1] - 1)
                        copy = next_turn(copy)
                        neighbors.append(copy)
                    if self.can_move(facing_position, (facing_position[0], facing_position[1] + 1)) \
                            and (facing_position[0], facing_position[1] + 1) not in other_positions:  # can go to the east ?
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0], facing_position[1] + 1)
                        copy = next_turn(copy)
                        neighbors.append(copy)
            elif facing_position[1] > current_position[1]:  # check if come from west
                if self.can_move(facing_position, (facing_position[0], facing_position[1]+1)):  # can go to the east ?
                    if (facing_position[0], facing_position[1]+1) not in other_positions:  # not arrived on another player
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0], facing_position[1]+1)
                        copy = next_turn(copy)
                        neighbors.append(copy)
                else:
                    if self.can_move(facing_position, (facing_position[0]-1, facing_position[1])) \
                            and (facing_position[0]-1, facing_position[1]) not in other_positions:  # can go to the north ?
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0]-1, facing_position[1])
                        copy = next_turn(copy)
                        neighbors.append(copy)
                    if self.can_move(facing_position, (facing_position[0]+1, facing_position[1])) \
                            and (facing_position[0]+1, facing_position[1]) not in other_positions:  # can go to the south ?
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0]+1, facing_position[1])
                        copy = next_turn(copy)
                        neighbors.append(copy)
            elif facing_position[0] > current_position[0]:  # check if come from north
                if self.can_move(facing_position, (facing_position[0]+1, facing_position[1])):  # can go to the south ?
                    if (facing_position[0]+1, facing_position[1]) not in other_positions:  # not arrived on another player
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0]+1, facing_position[1])
                        copy = next_turn(copy)
                        neighbors.append(copy)
                else:
                    if self.can_move(facing_position, (facing_position[0], facing_position[1]-1)) \
                            and (facing_position[0], facing_position[1]-1) not in other_positions:  # can go to the west ?
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0], facing_position[1]-1)
                        copy = next_turn(copy)
                        neighbors.append(copy)
                    if self.can_move(facing_position, (facing_position[0], facing_position[1]+1)) \
                            and (facing_position[0], facing_position[1]+1) not in other_positions:  # can go to the east ?
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0], facing_position[1]+1)
                        copy = next_turn(copy)
                        neighbors.append(copy)
            elif facing_position[1] < current_position[1]:  # check if come from east
                if self.can_move(facing_position, (facing_position[0], facing_position[1]-1)):  # can go to the west ?
                    if (facing_position[0], facing_position[1]-1) not in other_positions:  # not arrived on another player
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0], facing_position[1]-1)
                        copy = next_turn(copy)
                        neighbors.append(copy)
                else:
                    if self.can_move(facing_position, (facing_position[0]-1, facing_position[1])) \
                            and (facing_position[0]-1, facing_position[1]) not in other_positions:  # can go to the north ?
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0]-1, facing_position[1])
                        copy = next_turn(copy)
                        neighbors.append(copy)
                    if self.can_move(facing_position, (facing_position[0]+1, facing_position[1])) \
                            and (facing_position[0]+1, facing_position[1]) not in other_positions:  # can go to the south ?
                        copy = deepcopy(self)
                        copy.p_positions[self.turn] = (facing_position[0]+1, facing_position[1])
                        copy = next_turn(copy)
                        neighbors.append(copy)
        # ---------------------------------------------
        neighbors = []
        if self.exists_winner() != -1:  # handle victory
            return neighbors
        current_position = self.p_positions[self.turn]
        other_positions = [self.p_positions[p_id] for p_id in [i for i in range(self.n)] if p_id != self.turn]  # other players' positions

        if self.can_move((current_position[0] - 1, current_position[1]), current_position):  # try to move player to the north
            if (current_position[0] - 1, current_position[1]) in other_positions:  # handle facing
                facing((current_position[0] - 1, current_position[1]))
            else:
                copy = deepcopy(self)
                copy.p_positions[self.turn] = (current_position[0] - 1, current_position[1])
                copy = next_turn(copy)
                neighbors.append(copy)
        if self.can_move((current_position[0], current_position[1]+1), current_position):  # try to move player to the east
            if (current_position[0], current_position[1]+1) in other_positions:  # handle facing
                facing((current_position[0], current_position[1]+1))
            else:
                copy = deepcopy(self)
                copy.p_positions[self.turn] = (current_position[0], current_position[1]+1)
                copy = next_turn(copy)
                neighbors.append(copy)
        if self.can_move((current_position[0]+1, current_position[1]), current_position):  # try to move player to the south
            if (current_position[0]+1, current_position[1]) in other_positions:  # handle facing
                facing((current_position[0]+1, current_position[1]))
            else:
                copy = deepcopy(self)
                copy.p_positions[self.turn] = (current_position[0]+1, current_position[1])
                copy = next_turn(copy)
                neighbors.append(copy)
        if self.can_move((current_position[0], current_position[1] - 1), current_position):  # try to move player to the west
            if (current_position[0], current_position[1] - 1) in other_positions:  # handle facing
                facing((current_position[0], current_position[1] - 1))
            else:
                copy = deepcopy(self)
                copy.p_positions[self.turn] = (current_position[0], current_position[1] - 1)
                copy = next_turn(copy)
                neighbors.append(copy)

        if self.walls[self.turn] > 0:  # check if player has any walls left
            # try to place a horizontal wall
            for i in range(8):
                for j in range(8):
                    if self.can_place(True, (i, j)):
                        copy = deepcopy(self)
                        copy.h_walls.add((i, j))
                        copy.walls[self.turn] -= 1
                        copy = next_turn(copy)
                        neighbors.append(copy)
            # try to place a vertical wall
            for i in range(8):
                for j in range(8):
                    if self.can_place(False, (i, j)):
                        copy = deepcopy(self)
                        copy.v_walls.add((i, j))
                        copy.walls[self.turn] -= 1
                        copy = next_turn(copy)
                        neighbors.append(copy)
        return neighbors

    def __hash__(self):
        return hash((tuple(self.p_positions), frozenset(self.h_walls), frozenset(self.v_walls), self.turn))

    def __eq__(self, other):
        assert isinstance(other, State)
        return self.n == other.n and self.turn == other.turn and self.p_positions == other.p_positions \
            and np.array_equal(self.h_walls, other.h_walls) and np.array_equal(self.v_walls, other.v_walls)

    def __str__(self):
        s = f"players' position: p.0: {self.p_positions[0]}, p.1: {self.p_positions[1]}\n" \
            f"horizontal walls: {self.h_walls}\n" \
            f"vertical walls: {self.v_walls}\n"
        return s
