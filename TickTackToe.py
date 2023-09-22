from math import pow


def make_move(board: list, move: tuple, player_id: int):
    """move(x,y)"""
    if player_id != 1 and player_id != 2:
        print("INVALID PLAYER_ID")
        return False

    if len(move) != 2:
        print("INVALID MOVE:WRONG NUMBER OF DIMENSIONS")
        return False

    x, y = move

    if not ((-1 < x < 3) and (-1 < y < 3)):
        print("INVALID MOVE:OUT OF RANGE")
        return False

    if board[y][x] != 0:
        print("INVALID MOVE:OCUPIED SPACE")
        return False

    board[y][x] = player_id
    return True


def new_board():
    return [[0 for i in range(3)] for j in range(3)]


def board_to_int(board):
    """_ = 0, x = 1, o = 2"""

    sum = 0

    e = 0
    for row in board:
        for tile in row:
            if tile == 0:
                sum += 0
            elif tile == 1:
                sum += 1 * pow(3, e)
            elif tile == 2:
                sum += 2 * pow(3, e)
            e += 1

    return int(sum)


def int_to_board(x: int):

    if x >= pow(3, 9):
        return False

    board = [["_" for h in range(3)] for p in range(3)]
    # board[row][col]

    for e in range(8, -1, -1):
        d = x // (int(pow(3, e)))
        # print("D", e, d)
        if e > 5:
            board[2][e - 6] = d
        elif e > 2:
            board[1][e - 3] = d
        else:
            board[0][e] = d
        x -= d * int(pow(3, e))
        # print("x", x)

    return board


def check_for_win(board):
    # todo
    pass


def print_board(board):
    symbols = ["_", "x", "o"]
    for y in board:
        for x in y:
            print(symbols[x], end="")
        print("")


board = new_board()
# [y][x]
print_board(int_to_board(19682))
