import numpy
from math import inf


class TTT:
    """ Tic-tac-toe with MiniMax """

    PLAYER = -1  # MIN
    COMPUTER = +1  # MAX
    EMPTY = 0  # Empty cell

    __SYMBOLS = {
        PLAYER: 'X',
        COMPUTER: 'O'
    }

    @classmethod
    def __symbol(cls, value):
        return cls.__SYMBOLS.get(value, ' ')

    def __init__(self):
        self.__board = [
            [TTT.EMPTY, TTT.EMPTY, TTT.EMPTY],
            [TTT.EMPTY, TTT.EMPTY, TTT.EMPTY],
            [TTT.EMPTY, TTT.EMPTY, TTT.EMPTY],
        ]

    def __is_full(self):
        return TTT.EMPTY not in numpy.array(self.__board)

    def __win_states(self):
        return [
            # Rows
            [self.__board[0][0], self.__board[0][1], self.__board[0][2]],
            [self.__board[1][0], self.__board[1][1], self.__board[1][2]],
            [self.__board[2][0], self.__board[2][1], self.__board[2][2]],
            # Columns
            [self.__board[0][0], self.__board[1][0], self.__board[2][0]],
            [self.__board[0][1], self.__board[1][1], self.__board[2][1]],
            [self.__board[0][2], self.__board[1][2], self.__board[2][2]],
            # Diagonals
            [self.__board[0][0], self.__board[1][1], self.__board[2][2]],
            [self.__board[2][0], self.__board[1][1], self.__board[0][2]],
        ]

    def __winner(self, who):
        return [who, who, who] in self.__win_states()

    def __open_paths(self, who):
        paths = 0
        for s in self.__win_states():
            if -who not in s:
                paths += 1
        return paths

    def __empty_cells(self):
        cells = []
        for x, row in enumerate(self.__board):
            for y, cell in enumerate(row):
                if cell == TTT.EMPTY:
                    cells.append([x, y])
        return cells

    def __evaluate(self):
        # Positive if IA (i.e., MAX) has the advantage
        return self.__open_paths(TTT.COMPUTER) - self.__open_paths(TTT.PLAYER)

    def __find_best_move(self, who, level):
        row = col = None
        score = who * -inf
        # Simulate move for IA
        for cell in self.__empty_cells():
            x, y = cell[0], cell[1]
            # Register my move
            self.__board[x][y] = who
            if self.__winner(who):
                s = who * inf
            elif self.__is_full():
                s = 0
            elif level == 0:
                # Compute score with evaluation function
                s = self.__evaluate()
            else:
                # Evaluate board from the opponent's perspective
                s, r, c = self.__find_best_move(-who, level - 1)
            # Check if move is best so far
            if (who * s >= who * score):
                score, row, col = s, x, y
            # Unregister my move
            self.__board[x][y] = TTT.EMPTY
        return score, row, col

    def __print_board(self):
        print(f"\nBOARD [{self.__evaluate()}]")
        print("   0 1 2")
        for i in range(3):
            print(f"  +-+-+-+\n{i} ", end="")
            for j in range(3):
                print(f"|{TTT.__symbol(self.__board[i][j])}", end="")
            print("|")
        print("  +-+-+-+")

    def play(self):

        level = max(int(input("Enter depth (>= 1) of evaluation tree: ")), 1)
        turn = TTT.PLAYER
        self.__print_board()

        while True:
            if turn == TTT.PLAYER:
                while True:
                    i = int(input("Row: "))
                    j = int(input("Column: "))
                    if i >= 0 and j >= 0 and i <= 2 and j <= 2 and self.__board[i][j] == TTT.EMPTY:
                        # Valid cell
                        break
                    print("Invalid cell, please retry...")
                self.__board[i][j] = TTT.PLAYER
            else:
                s, r, c = self.__find_best_move(TTT.COMPUTER, level - 1)
                print(f"\nComputer plays: ({r},{c}) [{s}]")
                self.__board[r][c] = TTT.COMPUTER
            self.__print_board()
            # Did last move lead to victory?
            if self.__winner(turn):
                print(f"\nWINNER: {TTT.__symbol(turn)}")
                break
            elif self.__is_full():
                print("\nNO WINNER")
                break
            # Continue game with other player
            turn = -turn


if __name__ == '__main__':
    ttt = TTT()
    ttt.play()
