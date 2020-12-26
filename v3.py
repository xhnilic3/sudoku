from math import sqrt
from time import time

with open("data/2006.txt") as file:
    data = file.read()

puzzle = []

for item in data:
    if item.isnumeric():
        puzzle.append(int(item))
    elif item == ' ' or item == '.':
        puzzle.append(0)

puzzle_length = len(puzzle)

n = int(sqrt(puzzle_length))

playground = []

for i in range(n):
    line = []
    for j in range(n):
        line.append(puzzle[i * n + j])
    playground.append(line)


def print_playground(playground):
    for line in playground:
        print(line)


# noinspection PyShadowingNames
def find_empty(playground):
    for row in range(len(playground)):
        for col in range(len(playground[0])):
            if playground[row][col] == 0:
                return row, col

    return None


def valid(playground, num, pos):
    for row_item in range(len(playground[0])):
        if playground[pos[0]][row_item] == num and pos[1] != row_item:
            return False

    for col_item in range(len(playground)):
        if playground[col_item][pos[1]] == num and pos[0] != col_item:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for box_row in range(box_y * 3, box_y * 3 + 3):
        for box_col in range(box_x * 3, box_x * 3 + 3):
            if playground[box_row][box_col] == num and (box_row, box_col) != pos:
                return False

    return True


def solve(playground):
    find = find_empty(playground)
    if not find:
        return True
    else:
        row, col = find
    sample = reduce_possibilities(row, col)
    for i in sample:
        if valid(playground, i, (row, col)):
            playground[row][col] = i

            if solve(playground):
                return True

            playground[row][col] = 0

    return False


def box_range(num):
    if num % int(sqrt(n)) == 0:
        return num, num + 1, num + 2
    elif num % int(sqrt(n)) == 1:
        return num - 1, num, num + 1
    elif num % int(sqrt(n)) == 2:
        return num - 2, num - 1, num


def row_remove(whole_set, row):
    return whole_set - set(playground[row])


def col_remove(whole_set, col):
    candidates = []
    for row in range(9):  # TODO 9 is magic number
        candidates.append(playground[row][col])
    return whole_set - set(candidates)


def box_remove(whole_set, row, col):
    candidates = []
    for row in box_range(row):
        for col in box_range(col):
            candidates.append(playground[row][col])
    return whole_set - set(candidates)


def reduce_possibilities(row, col):
    whole_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    whole_set = row_remove(whole_set, row)
    whole_set = col_remove(whole_set, col)
    whole_set = box_remove(whole_set, row, col)
    return whole_set


def check_for_only_possibility(playground, i, j):
    pass


start_time = time()
solve(playground)
print("Final time: %s s" % (time() - start_time))
print_playground(playground)
