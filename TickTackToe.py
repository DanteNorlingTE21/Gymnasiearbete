from math import pow, factorial
import threading


class TrainedAI:
    pass


kids = 0


class TreeBranch:
    def __init__(
        self,
        board: int,
        parent: "TreeBranch",
        currentPlayerMarker,
        start,
        depth: int = 0,
    ) -> None:
        # global kids
        # kids += 1
        # print(kids)
        self.children = []
        self.marker = currentPlayerMarker
        self.state = board
        self.parent = parent
        self.startDepth = start
        self.depth = depth
        self.value = {1: 0, 2: 0}

        self.getValue()

    def getValue(self):
        if check_for_win(self.state)[0] == True:
            self.updateTree(1, self.marker)
            return
        elif check_for_win(self.state)[0] == "TIE":
            self.updateTree(0, self.marker)
            return

        possibleMoves = []
        for y in range(3):
            for x in range(3):
                currentBoard = int_to_board(self.state).copy()
                if currentBoard[y][x] == 0:
                    currentBoard[y][x] = self.marker
                    possibleMoves.append(board_to_int(currentBoard))

        for move in possibleMoves:
            n = check_for_win(move)
            if n[0] == True:
                self.updateTree(1, self.marker)
            elif n[0] == "TIE":
                self.updateTree(0, self.marker)
                # self.updateTree(1, 1 if self.marker == 2 else 2)
            else:
                self.children.append(
                    TreeBranch(
                        move,
                        self,
                        1 if self.marker == 2 else 2,
                        self.startDepth,
                        self.depth + 1,
                    )
                )

    def updateTree(self, deltaValue, marker):
        if marker in self.value.keys():
            """
            print(
                "Tie dephth", self.depth
            ) if deltaValue == 1 and self.depth + self.startDepth > 4 else None
            """
            self.value[marker] += deltaValue  # * factorial(
            #    9 - (self.startDepth + self.depth)
            # )
            # self.value[2 if marker == 1 else 1] += -deltaValue * 0.5
        else:
            self.value[marker] = deltaValue
        if self.depth != 0:
            # print(self.value[marker])
            # print(self.parent)
            self.parent.updateTree(deltaValue / 10, marker)


class SetAlgorithm:
    def __init__(self, marker) -> None:
        if not (marker == 1 or marker == 2):
            raise Exception("INVALID MARKER")
        self.marker = marker

    def bestMove(self, board: int, turn: int = 0):
        trees = []
        possibleMoves = []
        for y in range(3):
            for x in range(3):
                boardArray = int_to_board(board)
                if boardArray[y][x] == 0:
                    boardArray[y][x] = self.marker
                    possibleMoves.append(board_to_int(boardArray))

        print(possibleMoves)
        for move in possibleMoves:
            # print("TREE TIME")
            if check_for_win(move)[0] == True:
                return move
            trees.append(TreeBranch(move, self, 1 if self.marker == 2 else 2, turn, 0))

        # print("DELTA TIME")
        opponentMarker = 1 if self.marker == 2 else 2
        # bestTree = trees[0]
        bestDelta = trees[0].value[self.marker] - trees[0].value[opponentMarker]
        # winPercent = trees[0].value[self.marker] / (
        #    abs(trees[0].value[self.marker]) + abs(trees[0].value[opponentMarker])
        # )
        bestTree = trees[0]
        # print("WIN PERCENT", winPercent)
        for tree in trees:
            print(
                tree.value,
            )
            """
            print(
                tree.value[self.marker]
                / (
                    abs(trees[0].value[self.marker])
                    + abs(trees[0].value[opponentMarker])
                ),
            )"""
            print(tree.value[self.marker] - tree.value[opponentMarker])
            print_board(int_to_board(tree.state))
            # print(self.marker, opponentMarker)

            """

            if (
                tree.value[self.marker]
                / (
                    abs(trees[0].value[self.marker])
                    + abs(trees[0].value[opponentMarker])
                )
                > winPercent            ):
                bestTree = tree
                winPercent = tree.value[self.marker] / (
                    abs(trees[0].value[self.marker])
                    + abs(trees[0].value[opponentMarker])
                )
                """
            if (tree.value[self.marker] - tree.value[opponentMarker]) > bestDelta:
                bestTree = tree
                bestDelta = tree.value[self.marker] - tree.value[opponentMarker]

        # print("WIN PERCENT", winPercent)
        return bestTree.state


class Human:
    pass


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
    if isinstance(board, int):
        board = int_to_board(board)

    # row
    if board[0][0] == board[0][1] and board[0][0] == board[0][2] and board[0][0] != 0:
        return True, board[0][0]
    if board[1][0] == board[1][1] and board[1][0] == board[1][2] and board[1][0] != 0:
        return True, board[1][0]
    if board[2][0] == board[2][1] and board[2][0] == board[2][2] and board[2][0] != 0:
        return True, board[2][0]
    # column
    if board[0][0] == board[1][0] and board[0][0] == board[2][0] and board[0][0] != 0:
        return True, board[0][0]
    if board[0][1] == board[1][1] and board[0][1] == board[2][1] and board[0][1] != 0:
        return True, board[0][1]
    if board[0][2] == board[1][2] and board[0][2] == board[2][2] and board[0][2] != 0:
        return True, board[0][2]

    # diagonal
    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] != 0:
        return True, board[0][0]
    if board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] != 0:
        return True, board[0][2]

    tie = True

    for row in board:
        for tile in row:
            if tile == 0:
                tie = False
    if tie:
        return "TIE", 0

    return False, 0


def print_board(board):
    symbols = ["_", "x", "o"]
    for y in board:
        for x in y:
            print(symbols[x], end="")
        print("")


board = new_board()
print_board(board)
turn = 0
player2 = SetAlgorithm(2)

while True:
    player_move = input("Move:").split(",")
    player_move[0], player_move[1] = int(player_move[0]), int(player_move[1])
    if not make_move(board, (player_move[0], player_move[1]), 1):
        print("INVALID MOVE")
        continue
    turn += 1
    print_board(board)
    board = int_to_board(player2.bestMove(board_to_int(board), turn))
    turn += 1
    print()
    print_board(board)
    if check_for_win(board)[0] != False:
        print("Game Over")
        break
