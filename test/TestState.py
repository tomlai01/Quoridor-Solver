import unittest
from src import State


class TestState(unittest.TestCase):

    def setUp(self):
        self.state2 = State.State(2)

    def test_init_2(self):
        self.assertEqual(2, self.state2.n)
        self.assertEqual(0, self.state2.turn)
        self.assertEqual(0, len(self.state2.h_walls))
        self.assertEqual(0, len(self.state2.v_walls))
        self.assertEqual([(0, 4), (8, 4)], self.state2.p_positions)
        self.assertEqual([(0, 8), (0, 0)], self.state2.goals)
        self.assertEqual([10, 10], self.state2.walls)

    def test_basic_neighbors_2(self):
        state = State.State(2)
        neighbors = state.get_neighbors()
        self.assertEqual(len(neighbors), 131)
        # wall is placed
        state = State.State(2)
        state.h_walls.add((0, 4))
        neighbors = state.get_neighbors()
        self.assertEqual(126, len(neighbors))

    def test_exist_winner_2(self):
        self.state2.p_positions[0] = (8, 5)
        self.assertEqual(0, self.state2.exists_winner())
        self.state2.p_positions[0] = (0, 4)
        self.state2.p_positions[1] = (0, 3)
        self.assertEqual(1, self.state2.exists_winner())

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
        # got out of board
        self.assertFalse(self.state2.can_move((0, 8), (0, 9)))
        self.assertFalse(self.state2.can_move((8, 8), (9, 8)))
        # basic move
        self.assertTrue(self.state2.can_move((0, 4), (0, 5)))
        # go to north
        self.assertTrue(self.state2.can_move((4, 4), (3, 4)))
        self.state2.h_walls.add((3, 4))
        self.assertFalse(self.state2.can_move((4, 4), (3, 4)))
        self.state2.h_walls.remove((3, 4))
        self.state2.h_walls.add((3, 3))
        self.assertFalse(self.state2.can_move((4, 4), (3, 4)))
        self.state2.h_walls.remove((3, 3))
        # go to east
        self.assertTrue(self.state2.can_move((4, 4), (4, 5)))
        self.state2.v_walls.add((4, 4))
        self.assertFalse(self.state2.can_move((4, 4), (4, 5)))
        self.state2.v_walls.remove((4, 4))
        self.state2.v_walls.add((3, 4))
        self.assertFalse(self.state2.can_move((4, 4), (4, 5)))
        self.state2.v_walls.remove((3, 4))
        # go to south
        self.assertTrue(self.state2.can_move((4, 4), (5, 4)))
        self.state2.h_walls.add((4, 4))
        self.assertFalse(self.state2.can_move((4, 4), (5, 4)))
        self.state2.h_walls.remove((4, 4))
        self.state2.h_walls.add((4, 3))
        self.assertFalse(self.state2.can_move((4, 4), (5, 4)))
        self.state2.h_walls.remove((4, 3))
        # go to west
        self.assertTrue(self.state2.can_move((4, 4), (4, 3)))
        self.state2.v_walls.add((4, 3))
        self.assertFalse(self.state2.can_move((4, 4), (4, 3)))
        self.state2.v_walls.remove((4, 3))
        self.state2.v_walls.add((3, 3))
        self.assertFalse(self.state2.can_move((4, 4), (4, 3)))
        self.state2.v_walls.remove((3, 3))
        self.assertTrue(self.state2.can_move((4, 4), (4, 3)))

    def test_exists_solution_2(self):
        self.assertTrue(self.state2.exists_solution())
        self.state2.h_walls.add((4, 4))
        self.assertTrue(self.state2.exists_solution())
        self.state2.h_walls.add((4,2))
        self.assertTrue(self.state2.exists_solution())
        self.state2.h_walls.add((4,0))
        self.assertTrue(self.state2.exists_solution())
        self.state2.h_walls.add((4, 6))
        self.assertTrue(self.state2.exists_solution())
        self.state2.h_walls.add((3, 7))
        self.assertTrue(self.state2.exists_solution())
        self.state2.v_walls.add((3, 6))
        self.assertFalse(self.state2.exists_solution())

    def test_can_place_2(self):
        # horizontal wall tests
        self.state2.h_walls.add((4, 4))
        self.assertTrue(self.state2.can_place(True, (3,3)))
        self.assertTrue(self.state2.can_place(False, (3, 3)))
        self.assertFalse(self.state2.can_place(False, (4, 4)))
        self.assertTrue(self.state2.can_place(True, (3, 4)))
        self.assertFalse(self.state2.can_place(True, (4, 3)))
        self.assertTrue(self.state2.can_place(True, (5, 4)))
        self.assertFalse(self.state2.can_place(True, (4, 5)))
        self.state2.h_walls.remove((4, 4))
        # vertical wall tests
        self.state2.v_walls.add((4, 4))
        self.assertTrue(self.state2.can_place(False, (3, 3)))
        self.assertTrue(self.state2.can_place(True, (3, 3)))
        self.assertFalse(self.state2.can_place(True, (4, 4)))
        self.assertTrue(self.state2.can_place(False, (4, 3)))
        self.assertFalse(self.state2.can_place(False, (3, 4)))
        self.assertTrue(self.state2.can_place(False, (4, 5)))
        self.assertFalse(self.state2.can_place(False, (5, 4)))
        self.state2.v_walls.remove((4, 4))
        # no solutions
        self.state2.v_walls.add((0, 3))
        self.state2.v_walls.add((0, 4))
        self.assertFalse(self.state2.can_place(True, (1, 4)))
        self.state2.v_walls.remove((0, 3))
        self.assertTrue(self.state2.can_place(False, (0, 3)))
        self.state2.h_walls.add((1, 4))
        self.assertFalse(self.state2.can_place(False, (0, 3)))

    def test_facing_neighbor_2(self):
        self.state2.p_positions[0] = (1, 4)
        self.state2.p_positions[1] = (2, 4)
        # without wall
        neighbors = self.state2.get_neighbors()
        positions = [neighbor.p_positions for neighbor in neighbors]
        self.assertTrue([(3, 4), (2, 4)] in positions)
        self.assertFalse([(2, 3), (2, 4)] in positions)
        self.assertFalse([(2, 5), (2, 4)] in positions)
        # with wall behind
        self.state2.h_walls.add((2,4))
        neighbors = self.state2.get_neighbors()
        positions = [neighbor.p_positions for neighbor in neighbors]
        self.assertFalse([(3, 4), (2, 4)] in positions)
        self.assertTrue([(2, 3), (2, 4)] in positions)
        self.assertTrue([(2, 5), (2, 4)] in positions)
        # add wall on a side
        self.state2.v_walls.add((1, 4))
        neighbors = self.state2.get_neighbors()
        positions = [neighbor.p_positions for neighbor in neighbors]
        self.assertFalse([(2, 5), (2, 4)] in positions)
        self.assertTrue([(2, 3), (2, 4)] in positions)
        self.state2.v_walls.add((2, 3))
        neighbors = self.state2.get_neighbors()
        positions = [neighbor.p_positions for neighbor in neighbors]
        self.assertFalse([(2, 5), (2, 4)] in positions)
        self.assertFalse([(2, 3), (2, 4)] in positions)

    def test_hash(self):
        state1 = State.State(2)
        state2 = State.State(2)
        self.assertTrue(hash(state1) == hash(state2))
        state1.turn = 1
        self.assertFalse(hash(state1) == hash(state2))
        state1.turn = 0
        state1.p_positions[0] = (1,4)
        self.assertFalse(hash(state1) == hash(state2))
        state1.p_positions[0] = (0, 4)
        state1.h_walls.add((2, 3))
        self.assertFalse(hash(state1) == hash(state2))
        state1.h_walls.remove((2, 3))
        state1.v_walls.add((2,3))
        self.assertFalse(hash(state1) == hash(state2))
        state1.v_walls.remove((2,3))
        self.assertTrue(hash(state1) == hash(state2))



