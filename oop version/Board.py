import random, json
class Board:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.bin_highlight_map = [[0 for _ in range(9)] for _ in range(9)]
        self.block_map = [[0 for _ in range(9)] for _ in range(9)]

    def get_cell(self, row, col):
        return self.board[row][col]

    def clear_highlights(self):
        self.bin_highlight_map[:] = [[0 for _ in range(9)] for _ in range(9)]  # [:] keeps the list and clears it, doesn't create a new one

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


    def load_puzzle(self):
        with open('puzzles.json', 'r') as f:
            simple_puzzles = json.load(f)

        puzzle = random.choice(simple_puzzles)
        for i in range(81):
            self.board[i // 9][i % 9] = puzzle[i]

        # rules
        # after num input change all the places in the created array to 1 in these cases:
        # 1. all input nums
        # 2. their entire horizontal axis
        # 3. their entire vertical axis
        # 4. their entire block

    def fill_binary_highlight_array(self, num):
        for row in range(9):
            for column in range(9):
                if self.board[row][column] == num:
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
                    print(f"\033[1m\033[31m{self.board[row][column]}\033[0m", end=" ")
                elif (row // 3 + column // 3) % 2 == 0:
                    print(f"\033[90m{self.board[row][column]}\033[0m", end=" ")
                else:
                    print(f"{self.board[row][column]}", end=" ")
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

    def is_solved(self):
        for row in range(9):
            for column in range(9):
                if self.board[row][column] == 0:
                    return False

        return True