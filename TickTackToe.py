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

    if board[y][x] != "_":
        print("INVALID MOVE:OCUPIED SPACE")
        return False

    board[y][x] = "x" if player_id == 1 else "o"
    return True


def new_board():
    return [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"],
    ]


def board_to_ints(board, player_id):
    output = []

    for y in board:
        for x in y:
            if x == "_":
                output.append(0)
            elif x == "x":
                if player_id == 1:
                    output.append(1)
                else:
                    output.append(-1)
            elif x == "o":
                if player_id == 1:
                    output.append(-1)
                else:
                    output.append(1)
    return output


def print_board(board):
    for y in board:
        for x in y:
            print(x, end="")
        print("")


board = new_board()
# [y][x]

make_move(board, (2, 2), 1)
make_move(board, (1, 1), 1)
make_move(board, (0, 0), 1)
make_move(board, (2, 0), 2)
make_move(board, (0, 2), 2)
print_board(board)
print(board_to_ints(board, 1))
print(board_to_ints(board, 2))
