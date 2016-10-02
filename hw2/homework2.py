############################################################
# CIS 521: Homework 2
############################################################

student_name = "Ricky Rajani"

############################################################
# Imports
############################################################
import random
import copy
import math

############################################################
# Section 1: N-Queens
############################################################


def num_placements_all(n):
    if n == 0:
        return 0

    result = 1
    cnt = 0
    while cnt < n:
        result *= n ** 2 - cnt
        cnt += 1
    return result


def num_placements_one_per_row(n):
    return math.factorial(n)


def n_queens_valid(board):
    for i, x in enumerate(board):
        if i < len(board) - 1:
            cnt = 1
            for y in board[i + 1:]:
                if x == y or y == x - cnt or y == x + cnt:
                    return False
                cnt += 1
    return True


def n_queens_solutions(n):
    result = [[]]
    for col in range(n):
        result = (sol + [x] for sol in result for x in range(n) if not (n_queens_helper(x, sol)))
    return result


def n_queens_helper(row, queens):
    return row in queens or any(abs(row - x) == len(queens) - i for i, x in enumerate(queens))


############################################################
# Section 2: Lights Out
############################################################


class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.m = len(board)
        self.n = len(board[0])

    def get_board(self):
        return self.board

    def on_board(self, x, y):
        return x >= 0 and x < self.m and y >= 0 and y < self.n

    def perform_move(self, row, col):
        # flip box
        if self.on_board(row, col):
            self.board[row][col] = not self.board[row][col]

        # flip box above
        if self.on_board(row, col - 1):
            self.board[row][col - 1] = not self.board[row][col - 1]

        # flip box below
        if self.on_board(row, col + 1):
            self.board[row][col + 1] = not self.board[row][col + 1]

        # flip box to the left
        if self.on_board(row - 1, col):
            self.board[row - 1][col] = not self.board[row - 1][col]

        # flip box to the right
        if self.on_board(row + 1, col):
            self.board[row + 1][col] = not self.board[row + 1][col]

    def scramble(self):
        for i, row in enumerate(self.board):
            for col in row:
                if random.random() < 0.5:
                    self.perform_move(i, col)

    def is_solved(self):
        for row in range(self.m):
            for col in range(self.n):
                if self.board[row][col]:
                    return False
        return True

    def copy(self):
        return LightsOutPuzzle(copy.deepcopy(self.board))

    def successors(self):
        for row in range(self.m):
            for col in range(self.n):
                p = self.copy()
                p.perform_move(row, col)
                yield ((row, col), p)

    def find_solution(self):
        tuple_board = tuple(tuple(x) for x in self.board)
        try:
            return next(self.bfs_paths(tuple_board))
        except StopIteration:
            return None

    def bfs_paths(self, start):
        queue = [([], start)]
        states = set()
        while queue:
            (move, state) = queue.pop(0)
            states.add(state)
            l = [list(x) for x in state]
            c = LightsOutPuzzle(l)
            for next_state in c.successors():
                ns = tuple(tuple(x) for x in next_state[1].get_board())
                if ns not in states:
                    if self.is_solved_bfs(next_state[1].get_board()):
                        yield move + [next_state[0]]
                    else:
                        queue.append((move + [next_state[0]], ns))

    def is_solved_bfs(self, state):
        for row in range(self.m):
            for col in range(self.n):
                if state[row][col]:
                    return False
        return True


def create_puzzle(rows, cols):
    result = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(False)
        result.append(row)

    return LightsOutPuzzle(result)


############################################################
# Section 3: Linear Disk Movement
############################################################
class LinearDiskMovement(object):

    def __init__(self, n, length, disks):
        self.n = n
        self.length = length
        self.disks = list(disks)

    def successors(self):
        for i in range(len(self.disks)):
            if self.disks[i]:
                if i + 1 < self.length:
                    if self.disks[i + 1] == 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i + 1] = disk
                        yield ((i, i + 1), LinearDiskMovement(self.n, self.length, replace))

                if i + 2 < self.length:
                    if self.disks[i + 2] == 0 and self.disks[i + 1] != 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i + 2] = disk
                        yield ((i, i + 2), LinearDiskMovement(self.n, self.length, replace))

                if i - 1 >= 0:
                    if self.disks[i - 1] == 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i - 1] = disk
                        yield ((i, i - 1), LinearDiskMovement(self.n, self.length, replace))

                if i - 2 >= 0:
                    if self.disks[i - 2] == 0 and self.disks[i - 1] != 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i - 2] = disk
                        yield ((i, i - 2), LinearDiskMovement(self.n, self.length, replace))


def solve_identical_disks(length, n):
    try:
        return next(bfs_lines_identical(length, n))
    except StopIteration:
        return None


def bfs_lines_identical(length, n):
    start = [1 for x in range(n)]
    for x in range(length - n):
        start.append(0)
    r = list(reversed(copy.deepcopy(start)))

    if start == r:
        yield [()]

    encountered_states = set()
    line = LinearDiskMovement(n, length, start)
    encountered_states.add(tuple(line.disks))

    queue = [line]
    moves = {line: ()}
    top = {line: line}
    solutions = []

    while queue:
        disk_instance = queue.pop(0)

        for move, next_instance in disk_instance.successors():
            if tuple(next_instance.disks) not in encountered_states:
                moves[next_instance] = move
                top[next_instance] = disk_instance
                # check if solved
                if next_instance.disks == r:
                    curr = next_instance
                    while top[curr] != curr:
                        solutions.append(moves[curr])
                        curr = top[curr]
                    yield list(reversed(solutions))

                encountered_states.add(tuple(next_instance.disks))
                queue.append(next_instance)


def solve_distinct_disks(length, n):
    try:
        return next(bfs_lines_distinct(length, n))
    except StopIteration:
        return None


def bfs_lines_distinct(length, n):
    start = [x + 1 for x in range(n)]
    for x in range(length - n):
        start.append(0)
    r = list(reversed(copy.deepcopy(start)))

    if start == r:
        yield [()]

    encountered_states = set()
    line = LinearDiskMovement(n, length, start)
    encountered_states.add(tuple(line.disks))

    queue = [line]
    moves = {line: ()}
    top = {line: line}
    solutions = []

    while queue:
        disk_instance = queue.pop(0)

        for move, next_instance in disk_instance.successors():
            if tuple(next_instance.disks) not in encountered_states:
                moves[next_instance] = move
                top[next_instance] = disk_instance
                # check if solved
                if next_instance.disks == r:
                    curr = next_instance
                    while top[curr] != curr:
                        solutions.append(moves[curr])
                        curr = top[curr]
                    yield list(reversed(solutions))

                encountered_states.add(tuple(next_instance.disks))
                queue.append(next_instance)



############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
10 hours
"""

feedback_question_2 = """
Implementing the find_solution method was particularly challenging and difficult to understand at first.
"""

feedback_question_3 = """
I liked the interactive GUI for LightsOut.
"""
