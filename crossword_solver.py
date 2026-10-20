def read_file(filename="test_puzzle.txt"):
    """
    Opens the file, reads the words and board entries, and assigns them to different lists.

    Parameters:
        filename (str): Name of the file to read (default is 'test_puzzle.txt').

    Returns:
        tuple: (list, list)
            - A list of strings for words.
            - A list of strings for the board.
    """
    try:
        with open(filename, "r") as file:
            # Read all lines from the file
            lines = file.readlines()

            # Separate words and board
            words = []
            board = []
            reading_board = False

            for line in lines:
                line = line.strip()
                if not line:  # Empty line separates words and board
                    reading_board = True
                    continue

                if reading_board:
                    board.append(line)
                else:
                    words.append(line)

            # Check if the board is consistent
            if not check_consistency(board):
                raise ValueError("The board is not consistent. Rows must have the same length.")

            # Ensure we have both words and a board
            if not words or not board:
                raise ValueError("The file must contain both words and a board structure.")

            return words, board

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return [], []
    except ValueError as e:
        print(f"Error: {e}")
        return [], []



def check_consistency(board):
    """
    Checks whether all rows in the board are of the same length.

    Parameters:
        board (list): The board as a list of strings.

    Returns:
        bool: True if the board is consistent, False otherwise.
    """
    row_length = len(board[0]) if board else 0
    for row in board:
        if len(row) != row_length:
            return False
    return True

def create_board(board):
    """
    Converts the board from a list of strings to a list of lists.

    Parameters:
        board (list): The board as a list of strings.

    Returns:
        list: The board as a list of lists.
    """
    return [list(row) for row in board]

def identifier(words):
    """
    Creates a list of boolean values, initialized as False, for tracking word usage.

    Parameters:
        words (list): A list of strings representing words.

    Returns:
        list: A list of boolean values initialized to False.
    """
    return [False] * len(words)

def print_board(board):
    """
    Prints the board in a readable format, replacing forbidden spaces with '+'.

    Parameters:
        board (list): The board as a list of lists.

    Returns:
        None
    """
    for row in board:
        print(" ".join(str(cell) if cell != 0 else "+" for cell in row))

def print_board_w_c(board):
    """
    Prints the board with row and column coordinates for easier reference.

    Parameters:
        board (list): The board as a list of lists.

    Returns:
        None
    """
    print(" ", " ".join(f"C{col+1}" for col in range(len(board[0]))))
    for idx, row in enumerate(board):
        print(f"R{idx+1}", " ".join(str(cell) if cell != 0 else "+" for cell in row))

def print_wordlist(words, wstatus):
    """
    Prints the list of words with their usage status ('USED' or 'NOT USED').

    Parameters:
        words (list): A list of strings representing words.
        wstatus (list): A list of boolean values representing the usage status of words.

    Returns:
        None
    """
    print("Word List Status")
    for idx, (word, status) in enumerate(zip(words, wstatus)):
        print(f"W{idx+1} {word} {'USED' if status else 'NOT USED'}")

def check_entries(coordinates, wordno, board, words):
    """
    Checks the validity of coordinates and word number.

    Parameters:
        coordinates (list): [row number, column number].
        wordno (int): The word number.
        board (list): The board as a list of lists.
        words (list): A list of strings representing words.

    Returns:
        tuple: (bool, bool)
            - First value is True if coordinates are valid, else False.
            - Second value is True if word number is valid, else False.
    """
    rowno, colno = coordinates
    coord_valid = 0 < rowno <= len(board) and 0 < colno <= len(board[0])
    word_valid = 0 < wordno <= len(words)
    return coord_valid, word_valid

def check_location(board, words, coordinates, wordno, direction='H'):
    """
    Checks if the word can be placed at the given location in the specified direction.

    Parameters:
        board (list): The board as a list of lists.
        words (list): A list of strings representing words.
        coordinates (list): [row number, column number].
        wordno (int): The word number.
        direction (str): 'H' for horizontal, 'V' for vertical (default is 'H').

    Returns:
        tuple: (bool, int)
            - First value is True if placement is valid, else False.
            - Second value is 0 if valid, or an error code indicating the problem.
    """
    rowno, colno = coordinates
    word = words[wordno - 1]

    # Check if starting cell is a forbidden cell
    if board[rowno - 1][colno - 1] == 0:
        return False, 1

    if direction == 'H':
        # Check if word exceeds the board horizontally
        if colno - 1 + len(word) > len(board[0]):
            return False, 4
        # Check if the word fits the space horizontally
        for i in range(len(word)):
            if board[rowno - 1][colno - 1 + i] not in (1, word[i]):
                return False, 5
    elif direction == 'V':
        # Check if word exceeds the board vertically
        if rowno - 1 + len(word) > len(board):
            return False, 7
        # Check if the word fits the space vertically
        for i in range(len(word)):
            if board[rowno - 1 + i][colno - 1] not in (1, word[i]):
                return False, 8

    return True, 0

def check_word_fits(board, words, coordinates, wordno, direction='H'):
    """
    Checks if the word fits at the given coordinates and matches existing letters, if any.

    Parameters:
        board (list): The board as a list of lists.
        words (list): A list of strings representing words.
        coordinates (list): [row number, column number].
        wordno (int): The word number.
        direction (str): 'H' for horizontal, 'V' for vertical (default is 'H').

    Returns:
        tuple: (bool, int)
            - First value is True if the word fits, else False.
            - Second value is 0 if valid, or an error code indicating the problem.
    """
    rowno, colno = coordinates
    word = words[wordno - 1]

    if direction == 'H':
        for i in range(len(word)):
            if board[rowno - 1][colno - 1 + i] not in (1, word[i]):
                return False, 1
    elif direction == 'V':
        for i in range(len(word)):
            if board[rowno - 1 + i][colno - 1] not in (1, word[i]):
                return False, 2

    return True, 0

# Örnek kullanım:
# board = [[1, 1, 1], [0, 1, 0], [0, 1, 0]]
# words = ["GTU", "TECH"]
# result = solve_board(board, words)
# print(result)


def clear_board(board, wstatus):
    """
    Clears the board by resetting all letters to 1 and sets all word statuses to False.

    Parameters:
        board (list): The board as a list of lists.
        wstatus (list): A list of boolean values representing word usage statuses.

    Returns:
        None
    """
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] != 0:
                board[row][col] = 1

    for i in range(len(wstatus)):
        wstatus[i] = False
        
def decompose_command(str1):
    """
    Decomposes a move command into its components (word number, coordinates, direction).

    Parameters:
        str1 (str): The move command as a string.

    Returns:
        tuple: (int, int or None, list or None, str or None)
            - First value: 0 if all information is valid, -1 otherwise.
            - Second value: Word number if valid, None otherwise.
            - Third value: Coordinates [row, column] if valid, None otherwise.
            - Fourth value: Direction ('H' or 'V') if valid, None otherwise.
    """
    import re

    # Regular expression to parse the command
    match = re.search(r"W(\d+).*R(\d+).*C(\d+).*D([HVhv])?", str1)

    if not match:
        return -1, None, None, None

    try:
        wordno = int(match.group(1))
        row = int(match.group(2))
        col = int(match.group(3))
        direction = match.group(4).upper() if match.group(4) else 'H'

        return 0, wordno, [row, col], direction
    except (ValueError, AttributeError):
        return -1, None, None, None

def word_it(board, words, wstatus, coordinates, wordno, direction):
    """
    Places a word on the board if all checks are valid.

    Parameters:
        board (list): The board as a list of lists.
        words (list): A list of strings representing words.
        wstatus (list): A list of boolean values representing word usage statuses.
        coordinates (list): [row number, column number].
        wordno (int): The word number.
        direction (str): 'H' for horizontal, 'V' for vertical.

    Returns:
        bool: True if the word is placed successfully, False otherwise.
    """
    # Check if entries are valid
    coord_valid, word_valid = check_entries(coordinates, wordno, board, words)
    if not (coord_valid and word_valid):
        return False

    # Check if location is valid
    location_valid, _ = check_location(board, words, coordinates, wordno, direction)
    if not location_valid:
        return False

    # Check if word fits
    word_fits, _ = check_word_fits(board, words, coordinates, wordno, direction)
    if not word_fits:
        return False

    # Place the word on the board
    row, col = coordinates
    word = words[wordno - 1]

    if direction == 'H':
        for i in range(len(word)):
            board[row - 1][col - 1 + i] = word[i]
    elif direction == 'V':
        for i in range(len(word)):
            board[row - 1 + i][col - 1] = word[i]

    # Mark the word as used
    wstatus[wordno - 1] = True
    return True

def track_move(mvn, trackboard, coordinates, wordno, direction, board, wstatus):
    """
    Tracks the move by recording it into the move history.

    Parameters:
        mvn (int): Current move number.
        trackboard (list): List to track move history.
        coordinates (list): [row number, column number].
        wordno (int): The word number.
        direction (str): 'H' for horizontal, 'V' for vertical.
        board (list): The current state of the board as a list of lists.
        wstatus (list): A list of boolean values representing word usage statuses.

    Returns:
        int: Updated move number.
    """
    # Create a snapshot of the current board and word statuses
    board_snapshot = [row[:] for row in board]
    wstatus_snapshot = wstatus[:]

    # Append the move details to the trackboard
    trackboard.append((coordinates, wordno, direction, board_snapshot, wstatus_snapshot))

    # Increment the move number
    return mvn + 1

def solve_board(board, words):
    """
    Solves the board by attempting to place all words.

    Parameters:
        board (list): The board as a list of lists.
        words (list): A list of strings representing words.

    Returns:
        bool: True if the solution is found, False otherwise.
    """
    from itertools import product

    # Initialize word usage status
    wstatus = [False] * len(words)

    def backtrack(board, wstatus, word_index):
        if word_index == len(words):
            return True

        word = words[word_index]

        for row, col in product(range(1, len(board) + 1), range(1, len(board[0]) + 1)):
            for direction in ['H', 'V']:
                if word_it(board, words, wstatus, [row, col], word_index + 1, direction):
                    if backtrack(board, wstatus, word_index + 1):
                        return True
                    # Undo move
                    clear_board(board, wstatus)
        return False

    return backtrack(board, wstatus, 0)
