# comments
#
# 3.02 added all logic for highlighting which was the main goal of this project
#     all thats left is
#     1. adding actual playability by adding cell num replacement logic and implementing it into the already existent turn system
#     2. expanding the puzzles (proposition: easy medium and hard levels or some random sudoku level generator)


import random, os, json

# === DECLARE ARRAYS ===
board = [[0 for _ in range(9)] for _ in range(9)]
bin_highlight = [[0 for _ in range(9)] for _ in range(9)]
block_arr = [[0 for _ in range(9)] for _ in range(9)]


with open('puzzles.json', 'r') as f:
    easy_puzzles = json.load(f)




# === HELPER FUNCTIONS ===

# this is for cross-compatibility across platforms
def clear_terminal():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_num(is_retry = False):
    if is_retry:
        num = int(input("Incorrect input, please retry: "))
    else:
        num = int(input("Enter a number(1-9): "))

    if num < 1 or num > 9:
        return get_num(is_retry=True)

    return num

def set_horizontal_axis(highlight_row):
        for column in range(9):
                bin_highlight[highlight_row][column] = 1

def set_vertical_axis(highlight_column):
        for row in range(9):
                bin_highlight[row][highlight_column] = 1

def get_block_num(row, column):
    block_num = block_arr[row][column]
    return block_num

def set_entire_block(block_num):
    for row in range(9):
        for column in range(9):
            if block_arr[row][column] == block_num:
                bin_highlight[row][column] = 1


def check_puzzle_solved():
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                return False

    return True








# === FILL ARRAY FUNCTIONS ===

def load_puzzle():
    puzzle = random.choice(easy_puzzles)
    for i in range(81):
        board[i // 9][i % 9] = puzzle[i]


    # rules
    # after num input change all the places in the created array to 1 in these cases:
    # 1. all input nums
    # 2. their entire horizontal axis
    # 3. their entire vertical axis
    # 4. their entire block
def fill_binary_highlight_array(num):
    for row in range(9):
        for column in range(9):
            if board[row][column] == num:
                set_horizontal_axis(row) # set the entire axis to 1 in the bin highlight array
                set_vertical_axis(column) # set the entire axis to 1 in the bin highlight array
                set_entire_block(get_block_num(row, column)) # set the entire block in to 1 in the bin highlight array


def fill_block_arr():
    for block in range(9):
        block_num = block + 1
        block_row_start = (block // 3) * 3
        block_col_start = (block % 3) * 3
        for r in range(3):
            for c in range(3):
                block_arr[block_row_start + r][block_col_start + c] = block_num







# === PRINT FUNCTIONS ===

def print_board():
    for row in range(9):
        for column in range(9):
            if bin_highlight[row][column] == 1:
                print(f"\033[1m\033[31m{board[row][column]}\033[0m", end=" ")
            elif (row // 3 + column // 3) % 2 == 0:
                print(f"\033[90m{board[row][column]}\033[0m", end=" ")
            else:
                print(f"{board[row][column]}", end=" ")
        print()


def print_analysis():
    # print block array
    print("Block array:")
    for row in range(9):
        for column in range(9):
            if (row // 3 + column // 3) % 2 == 0:
                print(f"\033[90m{block_arr[row][column]}\033[0m", end=" ")
            else:
                print(f"{block_arr[row][column]}", end=" ")
        print()

    print()

    # print help binary highlight array
    print("Helping binary highlight array:")
    for row in range(9):
        for column in range(9):
            if (row // 3 + column // 3) % 2 == 0:
                print(f"\033[90m{bin_highlight[row][column]}\033[0m", end=" ")
            else:
                print(f"{bin_highlight[row][column]}", end=" ")
        print()

    print()



# === MAIN ===

def main():
    fill_block_arr()
    load_puzzle()
    solved = False
    turn = 0

    while not solved:
        turn += 1
        print(f"Turn: {turn}")
        print_board()
        num = get_num()
        bin_highlight[:] = [[0 for _ in range(9)] for _ in range(9)] # [:] keeps the list and clears it, doesn't create a new one
        fill_binary_highlight_array(num)
        clear_terminal()
        print_board()
        solved = check_puzzle_solved()
        print()

    print(f"Puzzle solved in {turn} turns!")

main()
