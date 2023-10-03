from math import pow


class TrainedAI:
    pass


kids = 0


class TreeBranch:
    def __init__(
        self, board: int, parent: "TreeBranch", currentPlayerMarker, depth: int = 0
    ) -> None:
        # global kids
        # kids += 1
        # print(kids)
        self.children = []
        self.marker = currentPlayerMarker
        self.state = board
        self.parent = parent
        self.depth = depth
        self.value = {}
        self.getValue()

    def getValue(self):
        if check_for_win(self.state) == True:
            self.updateTree(1, self.marker)
            return
        elif check_for_win(self.state) == "TIE":
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
            self.children.append(
                TreeBranch(move, self, 1 if self.marker == 2 else 2, self.depth + 1)
            )
        for child in self.children:
            child.getValue()

    def updateTree(self, deltaValue, marker):
        if marker in self.value.keys():
            self.value[marker] += deltaValue
        else:
            self.value[marker] = deltaValue
        if self.depth != 0:
            print(self.value[marker])
            print(self.parent)
            self.parent.updateTree(deltaValue, marker)


class SetAlgorithm:
    def __init__(self, marker) -> None:
        if not (marker == 1 or marker == 2):
            raise Exception("INVALID MARKER")
        self.marker = marker

    def bestMove(self, board: int):
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
            print("TREE TIME")
            trees.append(TreeBranch(move, self, 1 if self.marker == 2 else 2, 0))

        print("DELTA TIME")
        opponentMarker = 1 if self.marker == 2 else 2
        bestTree = trees[0]
        bestDelta = trees[0].values[self.marker] - trees[0].values[opponentMarker]
        for tree in trees:
            if (tree.values[self.marker] - tree.values[opponentMarker]) > bestDelta:
                bestTree = tree
                bestDelta = tree.values[self.marker] - tree.values[opponentMarker]
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
        return True
    if board[1][0] == board[1][1] and board[1][0] == board[1][2] and board[1][0] != 0:
        return True
    if board[2][0] == board[2][1] and board[2][0] == board[2][2] and board[2][0] != 0:
        return True
    # column
    if board[0][0] == board[1][0] and board[0][0] == board[2][0] and board[0][0] != 0:
        return True
    if board[0][1] == board[1][1] and board[0][1] == board[2][1] and board[0][1] != 0:
        return True
    if board[0][2] == board[1][2] and board[0][2] == board[2][2] and board[0][2] != 0:
        return True

    # diagonal
    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] != 0:
        return True
    if board[0][2] == board[1][1] and board[0][2] == board[0][2] and board[0][2] != 0:
        return True

    tie = True

    for row in board:
        for tile in row:
            if tile == 0:
                tie = False
    if tie:
        return "TIE"

    return False


def print_board(board):
    symbols = ["_", "x", "o"]
    for y in board:
        for x in y:
            print(symbols[x], end="")
        print("")


board = new_board()
while True:
    player2 = SetAlgorithm(2)
    print_board(board)
    player_move = input("Move:").split(",")
    player_move[0], player_move[1] = int(player_move[0]), int(player_move[1])
    make_move(board, (player_move[0], player_move[1]), 1)
    print_board(board)
    board = int_to_board(player2.bestMove(board_to_int(board)))
    print_board(board)
