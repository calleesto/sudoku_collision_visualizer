import random, json
from sudoku import Sudoku
class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.bin_highlight_map = [[0 for _ in range(9)] for _ in range(9)]
        self.block_map = [[0 for _ in range(9)] for _ in range(9)]

    def get_cell(self, row, column):
        return self.grid[row][column]

    def set_cell(self, row, column, value):
        self.grid[row][column] = value

    def _set_horizontal_axis(self, highlight_row):
        for column in range(9):
            self.bin_highlight_map[highlight_row][column] = 1

    def _set_vertical_axis(self, highlight_column):
        for row in range(9):
            self.bin_highlight_map[row][highlight_column] = 1

    def _get_block_num(self, row, column):
        block_num = self.block_map[row][column]
        return block_num

    def _set_entire_block(self, block_num):
        for row in range(9):
            for column in range(9):
                if self.block_map[row][column] == block_num:
                    self.bin_highlight_map[row][column] = 1

    def load_puzzle(self, difficulty=0.5):
        """
        difficulty ranges from 0.1 (almost solved) to 0.9 (very hard)
        """
        generated_puzzle = Sudoku(3).difficulty(difficulty) # 3 for 3x3 block sudoku

        for row in range(9):
            for column in range(9):
                cell_value = generated_puzzle.board[row][column]

                # library fills list with None values.. converting to 0s
                if cell_value is None:
                    self.grid[row][column] = 0
                else:
                    self.grid[row][column] = cell_value

        # rules
        # after num input change all the places in the created array to 1 in these cases:
        # 1. all input nums
        # 2. their entire horizontal axis
        # 3. their entire vertical axis
        # 4. their entire block

    def fill_binary_highlight_array(self, num):
        for row in range(9):
            for column in range(9):
                if self.grid[row][column] == num:
                    self._set_horizontal_axis(row)  # set the entire axis to 1 in the bin highlight array
                    self._set_vertical_axis(column)  # set the entire axis to 1 in the bin highlight array
                    self._set_entire_block(
                        self._get_block_num(row, column))  # set the entire block in to 1 in the bin highlight array

    def fill_block_arr(self):
        for block in range(9):
            block_num = block + 1
            block_row_start = (block // 3) * 3
            block_col_start = (block % 3) * 3
            for r in range(3):
                for c in range(3):
                    self.block_map[block_row_start + r][block_col_start + c] = block_num

    def print_board(self):
        for row in range(9):
            for column in range(9):
                if self.bin_highlight_map[row][column] == 1:
                    print(f"\033[1m\033[31m{self.grid[row][column]}\033[0m", end=" ")
                elif (row // 3 + column // 3) % 2 == 0:
                    print(f"\033[90m{self.grid[row][column]}\033[0m", end=" ")
                else:
                    print(f"{self.grid[row][column]}", end=" ")
            print()

    def print_analysis(self):
        # print block array
        print("Block array:")
        for row in range(9):
            for column in range(9):
                if (row // 3 + column // 3) % 2 == 0:
                    print(f"\033[90m{self.block_map[row][column]}\033[0m", end=" ")
                else:
                    print(f"{self.block_map[row][column]}", end=" ")
            print()

        print()

        # print help binary highlight array
        print("Helping binary highlight array:")
        for row in range(9):
            for column in range(9):
                if (row // 3 + column // 3) % 2 == 0:
                    print(f"\033[90m{self.bin_highlight_map[row][column]}\033[0m", end=" ")
                else:
                    print(f"{self.bin_highlight_map[row][column]}", end=" ")
            print()

        print()

    def clear_highlights(self):
        self.bin_highlight_map[:] = [[0 for _ in range(9)] for _ in range(9)]  # [:] keeps the list and clears it, doesn't create a new one

    def is_solved(self):
        for row in range(9):
            for column in range(9):
                if self.grid[row][column] == 0:
                    return False

        return True

    def check_move(self, row, column):
        # later implement the checking if cell is empty into the highlighting algorithm
        if self.grid[row][column] == 0 and self.bin_highlight_map[row][column] == 0:
            return True
        else:
            return False



