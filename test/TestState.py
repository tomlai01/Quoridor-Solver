import unittest
from src import State


class TestState(unittest.TestCase):

    def setUp(self):
        self.state2 = State.State(2)

    def test_init_2(self):
        self.assertEqual(self.state2.n, 2)
        self.assertEqual(self.state2.turn, 0)
        self.assertEqual(self.state2.h_walls.all(), 0)
        self.assertEqual(self.state2.v_walls.all(), 0)
        self.assertEqual(self.state2.p_positions, [(0, 4), (8, 4)])
        self.assertEqual(self.state2.goals, [(0, 8), (0, 0)])
        self.assertEqual(self.state2.walls, [10, 10])

    def test_exist_winner_2(self):
        self.state2.p_positions[0] = (8, 5)
        self.assertEqual(self.state2.exists_winner(), 0)
        self.state2.p_positions[0] = (0, 4)
        self.state2.p_positions[1] = (0, 3)
        self.assertEqual(self.state2.exists_winner(), 1)

    def test_can_move_2(self):
        try:
            self.state2.can_move((0, 4), (1, 5))
            raise AssertionError()
        except AssertionError:
            pass
        try:
            self.state2.can_move((0, 4), (0, 6))
            raise AssertionError()
        except AssertionError:
            pass
        try:
            self.state2.can_move((0, 4), (2, 4))
            raise AssertionError()
        except AssertionError:
            pass
        self.assertFalse(self.state2.can_move((0, 8), (0, 9)))
        self.assertFalse(self.state2.can_move((8, 8), (9, 8)))
        self.assertTrue(self.state2.can_move((0, 4), (0, 5)))
        self.assertTrue(self.state2.can_move((4, 4), (3, 4)))
        self.assertTrue(self.state2.can_move((4, 4), (4, 5)))
        self.assertTrue(self.state2.can_move((4, 4), (5, 4)))
        self.assertTrue(self.state2.can_move((4, 4), (4, 3)))

    def test_exists_solution_2(self):
        self.assertTrue(self.state2.exists_solution())
        self.state2.h_walls[4, 4:6] = 1
        self.assertTrue(self.state2.exists_solution())
        self.state2.h_walls[4, 2:4] = 1
        self.assertTrue(self.state2.exists_solution())
        self.state2.h_walls[4, 0:2] = 1
        self.assertTrue(self.state2.exists_solution())
        self.state2.h_walls[4, 6:8] = 1
        self.assertTrue(self.state2.exists_solution())
        self.state2.h_walls[3, 7:9] = 1
        self.assertTrue(self.state2.exists_solution())
        self.state2.v_walls[4:6, 6] = 1
        self.assertFalse(self.state2.exists_solution())


    def test_basic_neighbors_2(self):
        state = State.State(4)
        neighbors = state.get_neighbors(True)
        self.assertEqual(len(neighbors), 131)
        # wall is placed
        state = State.State(4)
        state.h_walls[1, 4:6] = 1
        neighbors = state.get_neighbors(True)
        self.assertEqual(len(neighbors), 128)

    def test_facing_neighbor_s(self):
        state = State.State(4)
        state.h_walls[1, 4:6] = 1
        state.p_positions[0] = (1,4)
        state.p_positions[1] = (1,5)
        neighbors = state.get_neighbors(True)

    def test_hash(self):
        state1 = State.State(2)
        state2 = State.State(2)
        print(state1 == state2)
        print(hash(state1) == hash(state2))
        state1.n = 3
        print(state1 == state2)
        print(hash(state1) == hash(state2))
        state1.n = 2
        print(state1 == state2)
        print(hash(state1) == hash(state2))
        state1.turn = 1
        print(state1 == state2)
        print(hash(state1) == hash(state2))
        state1.turn = 0
        print(state1 == state2)
        print(hash(state1) == hash(state2))
        state1.p_positions[0] = (1,4)
        print(state1 == state2)
        print(hash(state1) == hash(state2))
        state1.p_positions[0] = (0, 4)
        print(state1 == state2)
        print(hash(state1) == hash(state2))
        state1.h_walls[2, 3:5] = 1
        print(state1 == state2)
        print(hash(state1) == hash(state2))
        state1.h_walls[2, 3:5] = 0
        print(state1 == state2)
        print(hash(state1) == hash(state2))
        state1.v_walls[2, 3:5] = 1
        print(state1 == state2)
        print(hash(state1) == hash(state2))
        state1.v_walls[2, 3:5] = 0
        print(state1 == state2)
        print(hash(state1) == hash(state2))



