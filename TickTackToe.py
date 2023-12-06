from math import pow, factorial, log
import threading
from datetime import datetime
from keras.models import Sequential, load_model, save_model
from keras.layers import Dense
import numpy as np


DEBUG = False

class Human:
    def __init__(self, marker) -> None:
        self.marker = marker
        self.type = "Human"
    
    def getMove(self):
        while True:
            player_move = ["", ""]
            move_str = input("Move(Column,Row): ")

            player_move[0], player_move[1] = move_str[0], move_str[-1]
            try:
                player_move[0], player_move[1] = decipher_player_move(player_move)
            except TypeError:
                continue
            return player_move

class TrainedAI:
    """https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/"""
    def __init__(self, marker,randomness = 50,  new_model:bool = True) -> None:
        self.marker = marker
        self.type = "TrainedAI"
        self.randomness = randomness
        if new_model:
            self.network = Sequential()
            self.network.add(Dense(9, input_dim=9, activation="sigmoid"))
            self.network.add(Dense(9, activation="sigmoid"))
            self.network.add(Dense(9, activation="sigmoid"))
            self.network.add(Dense(9, activation="sigmoid"))
            self.network.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
        else:
            self.network = load_model("Models/model3.keras")

    def handleTrainingData(self, input_boards,output_boards):
        self.input_data = [getBiasedBoard(int_to_board(x), self.marker) for x in input_boards]
        self.output_data = [whatMoveWasMade(input_boards[x], output_boards[x]) for x in range(len(output_boards))]
        
    def readTrainingData(self, file):
        data = np.loadtxt(file, dtype='int', delimiter=',')
        inp = data[:, 0]
        out = data[:, 1]
        return inp, out
    
    def train(self, epochs=100, batch_size=10):
        input_boards, output_boards =self.readTrainingData("MoveLog/winningMoves.txt")
        self.handleTrainingData(input_boards, output_boards)
        self.network.fit(np.array(self.input_data), np.array(self.output_data), epochs=epochs, batch_size=batch_size)
    
    def getMove(self, board):
        prediction = self.network.predict(np.array([getBiasedBoard(board, self.marker)]))
        move_order = np.argsort(prediction[0])
        print(move_order) if DEBUG else None
        if self.randomness < np.random.randint(0,100):
            for i in range(-1,-10,-1):
                if make_move(board, (move_order[i]%3,move_order[i]//3), self.marker):
                    break
        else:
            while True:
                random_move = (np.random.randint(0,3),np.random.randint(0,3))
                if make_move(board, random_move, self.marker):
                    break


class TreeBranch:
    def __init__(
        self,
        board: int,
        parent: "TreeBranch",
        currentPlayerMarker,
        start,
        depth: int = 0,
    ) -> None:

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
        self.type = "SetAlgorithm"

    def getMove(self, board: int, turn: int = 0):
        trees = []
        possibleMoves = []
        for y in range(3):
            for x in range(3):
                boardArray = int_to_board(board)
                if boardArray[y][x] == 0:
                    boardArray[y][x] = self.marker
                    possibleMoves.append(board_to_int(boardArray))

        print(possibleMoves) if DEBUG else None
        if len(possibleMoves) == 9:
            return board_to_int([[0, 0, 0], [0, self.marker, 0], [0, 0, 0]])
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
            if DEBUG:
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
    print("  A  B  C")
    i = 1
    for y in board:
        print(i, end=" ")
        i += 1
        for x in y:
            print(symbols[x]," ", end="")
        print("")

def decipher_player_move(move:tuple):
    x = move[0] if not move[0].isdigit() else move[1]
    y = move[1] if move[1].isdigit() else move[0]

    if x.isdigit() and y.isdigit():
        print("INVALID MOVE:INVALID ROW AND COLUMN")
        return False
    elif not x.isdigit() and not y.isdigit():
        print("INVALID MOVE:INVALID ROW AND COLUMN")
        return False
    
    x = x.upper()
    
    if x == "A":
        x = 0
    elif x == "B":
        x = 1
    elif x == "C":
        x = 2
    else:
        print("INVALID MOVE:INVALID COLUMN")
        return False

    if y == "1":
        y = 0
    elif y == "2":
        y = 1
    elif y == "3":
        y = 2
    else:
        print("INVALID MOVE:INVALID ROW")
        return False

    return (x,y)

def whatMoveWasMade(board1, board2):
    if not (isinstance(board1, int) or isinstance(board1, np.int32)):
        board1 = board_to_int(board1)
    if not (isinstance(board2, int) or isinstance(board2, np.int32)):
        board2 = board_to_int(board2)
    deltaBoard = board2-board1
    if deltaBoard % 2 == 0:
        deltaBoard = deltaBoard/2

    index = round(log(deltaBoard,3))
    output = [0 for i in range(9)]
    output[index] = 1
    return output    

def getBiasedBoard(board, playerMarker):
    biasedBoard = [0 for i in range(9)]
    for y in range(3):
        for x in range(3):
            if board[y][x] == playerMarker:
                biasedBoard[x+y*3] = 1
            elif board[y][x] != 0:
                biasedBoard[x+y*3] = -1
    return biasedBoard

def game(player1,player2,log:bool = False):
    board = new_board()
    print_board(board)
    board_states = [0,]
    turn = 0
    players = [player1,player2]
    while True:
        if players[turn%2].type == "Human":
            if not make_move(board, (players[turn%2].getMove()), 1):
                print("INVALID MOVE")
                continue
        elif players[turn%2].type == "SetAlgorithm":
            board = int_to_board(players[turn%2].getMove(board_to_int(board), turn))
        elif players[turn%2].type == "TrainedAI":
            players[turn%2].getMove(board)
        turn += 1
        print()
        print_board(board)
        board_states.append(board_to_int(board))
        if check_for_win(board)[0] != False:
            print("Game Over")
            break
    winner = None if check_for_win(board)[1] == 0 else check_for_win(board)[1]
    print("Winner:", winner)
    if log:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        date = date.replace("/","-")
        date = date.replace(":","-")
        with open("Logged Games/"+"game"+date+".txt","w") as f:
            f.write("Game Log\n")
            f.write("Winner: "+str(winner)+"\n")
            f.write("Player1: "+player1.type+"\n")
            f.write("Player2: "+player2.type+"\n")
            f.write("Board States:\n")
            f.write(str(board_states))
            f.write("\n")
            f.write("Turns: "+str(turn)+"\n")
            f.write("Game End\n")
        with open("MoveLog/moves.txt", "a") as f:
            for i in range(len(board_states)-1):
                f.write(str(board_states[i])+","+str(board_states[i+1])+"\n")
    with open("MoveLog/winningMoves.txt", "a") as f:    
        if winner != None:
                if winner == 1:
                    for i in range(9):
                        if 2*i+1 >= len(board_states):
                            break
                        f.write(str(board_states[2*i])+","+str(board_states[2*i+1])+"\n")
                else:
                    for i in range(9):
                        if 2*i+2 >= len(board_states):
                            break
                        f.write(str(board_states[2*i+1])+","+str(board_states[2*i+2])+"\n")
        else:
            for i in range(len(board_states)-1):
                    f.write(str(board_states[i])+","+str(board_states[i+1])+"\n")


        
"""

player2 = SetAlgorithm(2)
player1 = Human(1)
game(player1,player2,True)

print(whatMoveWasMade(0, 729))
print(getBiasedBoard(int_to_board(729), 2))

subjekt = TrainedAI(1)
subjekt.train(epochs=1000, batch_size=10)
board = new_board()
subjekt.getMove(board)
print(board)
save_model(subjekt.network, "Models/model3.keras")
"""

player1 = TrainedAI(1,0, False)
player2 = TrainedAI(2,30 ,False)


for i in range(5):
    for i in range(100):
        if i%2 == 0:
            game(player1,player2,True)
        else:
            game(player2,player1,True)
    player1.train(epochs=300, batch_size=10)
    player1.randomness *= 0.85
    clear_file = open("MoveLog/winningMoves.txt", "w")
    clear_file.close()
else:
    save_model(player2.network, "Models/model3.keras")
"""

game(player2,player1,False)
"""


#973