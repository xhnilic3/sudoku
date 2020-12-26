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

priority = []

playground = []

counter = 0
depth = 0

for i in range(n):
    line = []
    for j in range(n):
        line.append(puzzle[i * n + j])
    playground.append(line)


def print_playground(playground):
    for line in playground:
        print(line)


def prioritization(playground):
    global priority
    for x in range(9):
        for y in range(9):
            if playground[x][y] == 0:
                record = []
                record.append(x)
                record.append(y)
                record.append(len(reduce_possibilities(x, y)))
                priority.append(record)


# noinspection PyShadowingNames
def find_empty(bo):
    for row in range(len(bo)):
        for col in range(len(bo[0])):
            if bo[row][col] == 0:
                return row, col

    return None


def valid(bo, num, pos):
    for row_item in range(len(bo[0])):
        if bo[pos[0]][row_item] == num and pos[1] != row_item:
            return False

    for col_item in range(len(bo)):
        if bo[col_item][pos[1]] == num and pos[0] != col_item:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for box_row in range(box_y * 3, box_y * 3 + 3):
        for box_col in range(box_x * 3, box_x * 3 + 3):
            if bo[box_row][box_col] == num and (box_row, box_col) != pos:
                return False

    return True


def solve(playground):
    global counter
    global depth
    if depth < 40:
        depth += 1
        if counter == len(priority):
            return True
        else:
            prioritization(playground)
            row = priority[counter][0]
            col = priority[counter][1]
            counter += 1
    else:
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


def solve2(playground):
    find = find_empty(playground)
    if not find:
        return True
    else:
        row, col = find
    sample = reduce_possibilities(row, col)
    for i in sample:
        if valid(playground, i, (row, col)):
            playground[row][col] = i

            if solve2(playground):
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


def skuska(arr):
    return arr[2]


# print_playground(playground)
start_time = time()
prioritization(playground)
priority.sort(key=lambda x: x[2])


# for line in priority:
#     print(line)
# # priority = sorted(priority, key=itemgetter(2))
# for record in priority:
#     print(record)
# print(len(priority[0]))
solve(playground)
print("algo time: ", time() - start_time)
print_playground(playground)
# # solve2(playground)
# print_playground(playground)

