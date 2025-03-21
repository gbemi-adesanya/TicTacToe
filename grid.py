from random import choice
# DPS means debug print statement

class Grid:
    def __init__(self, n):
        """
        :param n: int, the size of the grid
        """
        self.grid = [[" " for _ in range(n)] for _ in range(n)]
        self.winner = None

    def __str__(self):
        """
        string representation of Grid objects
        :return:
        """
        n = self.get_size()
        print("\t", end="")
        for col in range(n):
            print(col + 1, end=" "*5)           # col num
        print()

        col_delimiter = "  |  "
        for row in range(n):
            print(row + 1, end="\t")            # row num

            for col in range(n):
                print(self.grid[row][col], end="")
                if col < n - 1:
                    print(col_delimiter, end="")
            print()

            if row < n - 1:
                row_delimiter = "-" * (6 * n - 5)
                print("\t" + row_delimiter)
        return ""

    def get_size(self):
        """
        getter method
        :return: int, the size of the grid
        """
        return len(self.grid)

    def modify_cell(self, char, row, col):
        """
        Places player's character in the right cell
        :param char: str, the character to be placed
        :param row: int, the row number
        :param col: int, the column number
        """
        n = self.get_size()

        while True:
            try:
                if not (1 <= row <= n and 1 <= col <= n):
                    raise ValueError(f"Row and column indices must be between 1 and {n}.\n")

                # change for 0-indexing
                row -= 1
                col -= 1

                if self.grid[row][col] != " ":
                    raise ValueError(f"Cell is already occupied. Choose another.\n")

                self.grid[row][col] = char
                print(self)
                break

            except ValueError as error:
                print(error)
                row, col = map(int, input(f"Player {char}, where do you want to place your choice? e.g. 1 1: ").split())

    def status_check(self):
        """
        :return: str, the status of the game (win, draw, or game in progress)
        """
        def winner_check(cells):
            """
            helper function: checks if a winner exists in a group of cells
            :param cells: cells to check for winner
            :return: bool, winner or no
            """
            if all(cell == cells[0] and cell != " " for cell in cells):
                self.winner = cells[0]
                return True
            return False

        n = self.get_size()
        # rows
        for row in self.grid:
            if winner_check(row):         # The cells aren't empty and all contain the same value
                return f"Player {self.winner} wins!", True

        # columns
        for i in range(n):
            column = [self.grid[j][i] for j in range(n)]
            if winner_check(column):
                return f"Player {self.winner} wins!", True

        # diagonals
        neg_diag = [self.grid[i][i] for i in range(n)]
        pos_diag = [self.grid[i][n - i - 1] for i in range(n)]
        if winner_check(neg_diag) or winner_check(pos_diag):
            return f"Player {self.winner} wins!", True

        # draw
        if all(cell != " " for row in self.grid for cell in row):           # all spaces are filled and no winner
            return "Draw!", True

        return "Game in progress", False                                    # game in progress

    def empty_cells(self):
        """
        :return: a list of unoccupied cells (as tuples)
        """
        n = self.get_size()
        # Adjust indices for 1-based indexing
        return [(i + 1, j + 1) for i in range(n) for j in range(n) if self.grid[i][j] == " "]

    def computer_move(self, char, opponent_char):
        """
        Given the game state, choose the best possible move
        :return: tuple, the cell to place the computer's move
        """
        def win_block_strategy(char, opponent_char):
            """
            Check for a winning move and/or a blocking move.
            :param char: str, the first player (computer)
            :param opponent_char: str, the other player
            :return: tuple, the cell to place the computer's move
            """
            # check for win
            win_cell = best_move(char)
            if win_cell: return win_cell

            # check for block
            block_cell = best_move(opponent_char)
            if block_cell: return block_cell

            return None  # no winning or blocking

        def best_move(char):
            """
            Returns the cell of the best move to make
            :param char: the current player
            :return: tuple, the best move for the char
            """
            n = self.get_size()
            for row in range(n):
                for col in range(n):
                    if self.grid[row][col] == " ":
                        # Check winning or blocking
                        self.grid[row][col] = char
                        if self.status_check()[1]:  # status_check() returns True if there's a win (or a draw)
                            self.grid[row][col] = " "  # reset if there's a move
                            return (row + 1, col + 1)  # adjust for 1-based indexing
                        self.grid[row][col] = " "  # reset after if there's no move
            return None  # no move

        n = self.get_size()
        # 1. Win the game or block opponent from winning
        cell = win_block_strategy(char, opponent_char)
        if cell:
            self.modify_cell(char, cell[0], cell[1])
            return

        empty_cells = self.empty_cells()
        # 2. Play in the middle cell, since it has the greatest access
        row = col = n // 2
        if (row + 1, col + 1) in empty_cells:
            self.modify_cell(char, row + 1, col + 1)
            return

        # 3. Play in a random cell
        cell = choice(empty_cells)
        self.modify_cell(char, cell[0], cell[1])
