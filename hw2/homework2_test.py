import homework2 as hw
import unittest


class TestNQueens(unittest.TestCase):

    def test_num_placements_all(self):
        self.assertEqual(hw.num_placements_all(0), 0)
        self.assertEqual(hw.num_placements_all(1), 1)
        self.assertEqual(hw.num_placements_all(2), 12)
        self.assertEqual(hw.num_placements_all(4), 43680)
        self.assertEqual(hw.num_placements_all(8), 178462987637760)

    def test_num_placements_one_per_row(self):
        self.assertEqual(hw.num_placements_one_per_row(8), 40320)

    def test_n_queens_valid(self):
        self.assertEqual(hw.n_queens_valid([0, 0]), False)
        self.assertEqual(hw.n_queens_valid([0, 2]), True)
        self.assertEqual(hw.n_queens_valid([0, 1]), False)
        self.assertEqual(hw.n_queens_valid([0, 3, 1]), True)

    def test_n_queens_solutions(self):
        solutions = hw.n_queens_solutions(4)
        self.assertEqual(next(solutions), [1, 3, 0, 2])
        self.assertEqual(next(solutions), [2, 0, 3, 1])

        self.assertEqual(list(hw.n_queens_solutions(6)), [[1, 3, 5, 0, 2, 4], [2, 5, 1, 4, 0, 3],
                                                          [3, 0, 4, 1, 5, 2], [4, 2, 0, 5, 3, 1]])

        self.assertEqual(len(list(hw.n_queens_solutions(8))), 92)
        self.assertEqual(len(list(hw.n_queens_solutions(9))), 352)


class TestLightsOut(unittest.TestCase):
    def test_get_board(self):
        b = [[True, False], [False, True]]
        p = hw.LightsOutPuzzle(b)
        p.get_board()
        self.assertEqual(p.get_board(), [[True, False], [False, True]])

    def test_create_puzzle(self):
        p = hw.create_puzzle(2, 2)
        self.assertEqual(p.get_board(), [[False, False], [False, False]])

        p = hw.create_puzzle(2, 3)
        self.assertEqual(p.get_board(), [[False, False, False], [False, False, False]])

    def test_perform_move(self):
        p = hw.create_puzzle(3, 3)
        p.perform_move(1, 1)
        self.assertEqual(p.get_board(), [[False, True, False], [True,  True, True], [False, True, False]])

        p = hw.create_puzzle(3, 3)
        p.perform_move(0, 0)
        p.perform_move(2, 2)
        self.assertEqual(p.get_board(), [[True,  True,  False], [True,  False, True], [False, True, True]])

    def test_scramble(self):
        p = hw.create_puzzle(3, 3)
        p.scramble()

    def test_is_solved(self):
        b = [[True, False], [False, True]]
        p = hw.LightsOutPuzzle(b)
        self.assertEqual(p.is_solved(), False)

        b = [[False, False], [False, False]]
        p = hw.LightsOutPuzzle(b)
        self.assertEqual(p.is_solved(), True)

    def test_copy(self):
        p = hw.create_puzzle(3, 3)
        p2 = p.copy()
        self.assertEqual(p.get_board() == p2.get_board(), True)

        p = hw.create_puzzle(3, 3)
        p2 = p.copy()
        p.perform_move(1, 1)
        self.assertEqual(p.get_board() == p2.get_board(), False)

    # def test_successors(self):
    #     p = hw.create_puzzle(2, 2)
    #     for move, new_p in p.successors():
    #         print move, new_p.get_board()
    #
    #     for i in range(2, 6):
    #         p = hw.create_puzzle(i, i + 1)
    #         print len(list(p.successors()))

    def test_find_solution(self):
        p = hw.create_puzzle(2, 2)
        p.perform_move(1, 1)
        self.assertEqual(p.find_solution(), [(1, 1)])

        p = hw.create_puzzle(2, 3)
        for row in range(2):
            for col in range(3):
                p.perform_move(row, col)
        self.assertEqual(p.find_solution(), [(0, 0), (0, 2)])


class TestLightsOut(unittest.TestCase):
    def test_solve_identical_disks1(self):
        self.assertEqual(hw.solve_identical_disks(4, 2), [(0, 2), (1, 3)])

    def test_solve_identical_disks2(self):
        self.assertEqual(hw.solve_identical_disks(5, 2), [(0, 2), (1, 3), (2, 4)])

    def test_solve_identical_disks3(self):
        self.assertEqual(hw. solve_identical_disks(4, 3), [(1, 3), (0, 1)])

    def test_solve_identical_disks4(self):
        self.assertEqual(hw.solve_identical_disks(5, 3), [(1, 3), (0, 1), (2, 4), (1, 2)])

    def test_solve_distinct_disks1(self):
        s = [(0, 2), (2, 3), (1, 2)]
        self.assertEqual(hw.solve_distinct_disks(4, 2), s)

    def test_solve_distinct_disks2(self):
        s = [(1, 3), (0, 1), (2, 0), (3, 2), (1, 3), (0, 1)]
        self.assertEqual(hw.solve_distinct_disks(4, 3), s)

    def test_solve_distinct_disks3(self):
        s = [(0, 2), (1, 3), (2, 4)]
        self.assertEqual(hw.solve_distinct_disks(5, 2), s)

    def test_solve_distinct_disks4(self):
        s = [(1, 3), (2, 1), (0, 2), (2, 4), (1, 2)]
        self.assertEqual(hw.solve_distinct_disks(5, 3), s)

    def test_solve_distinct_disks5(self):
        s = [(1, 3), (0, 1), (2, 0), (3, 2), (1, 3), (0, 1)]
        self.assertEqual(hw.solve_distinct_disks(4, 3), s)

    def test_solve_distinct_disks6(self):
        self.assertEqual(hw.solve_distinct_disks(1, 1), [()])


if __name__ == '__main__':
    unittest.main()
