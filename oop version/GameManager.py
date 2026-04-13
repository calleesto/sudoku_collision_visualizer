import os
from Board import Board
class GameManager:
    def __init__(self):
        self.board = Board()
        self.timer = 0
        self.turn = 0

    # this is for cross-compatibility across platforms

    @staticmethod
    def clear_terminal():
        os.system('clear' if os.name == 'posix' else 'cls')

    def get_input(self, is_retry=False):
        if is_retry:
            num = int(input("Incorrect input, please retry: "))
        else:
            num = int(input("Enter a number(1-9): "))

        if num < 1 or num > 9:
            return self.get_input(is_retry=True)

        return num

    def play(self):
        self.board.fill_block_arr()
        self.board.load_puzzle()
        solved = False
        turn = 0

        while not solved:
            turn += 1
            print(f"Turn: {turn}")
            self.board.print_board()
            num = self.get_input()
            self.board.clear_highlights()
            self.board.fill_binary_highlight_array(num)
            self.clear_terminal()
            self.board.print_board()
            solved = self.board.is_solved()
            print()

        print(f"Puzzle solved in {turn} turns!")