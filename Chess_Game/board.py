import numpy as np
import pandas as pd
import math

def create_board():
    # Define the columns and rows labels
    columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    rows = ['8', '7', '6', '5', '4', '3', '2', '1']

    # Create the empty board
    board = pd.DataFrame(None, index=rows, columns=columns)

    # Set the starting positions of the pieces on the board
    board.loc['1', 'a'] = 'R'
    board.loc['1', 'b'] = 'N'
    board.loc['1', 'c'] = 'B'
    board.loc['1', 'd'] = 'Q'
    board.loc['1', 'e'] = 'K'
    board.loc['1', 'f'] = 'B'
    board.loc['1', 'g'] = 'N'
    board.loc['1', 'h'] = 'R'

    board.loc['2', :] = 'P'

    board.loc['7', :] = 'p'

    board.loc['8', 'a'] = 'r'
    board.loc['8', 'b'] = 'n'
    board.loc['8', 'c'] = 'b'
    board.loc['8', 'd'] = 'q'
    board.loc['8', 'e'] = 'k'
    board.loc['8', 'f'] = 'b'
    board.loc['8', 'g'] = 'n'
    board.loc['8', 'h'] = 'r'

    return board


def move_piece(board, move, is_white_turn, is_castling_valid):
    # Get the start and end positions from the move string
    start, end = move.split(',')

    # Convert the start and end positions to row and column indices
    start_row, start_col = 8 - int(start[1]), ord(start[0]) - 97
    end_row, end_col = 8 - int(end[1]), ord(end[0]) - 97

    # Get the piece being moved
    piece = board.iloc[start_row, start_col]

    # Check if the move is valid
    if is_valid_move(board, start_row, start_col, end_row, end_col, piece, is_white_turn, is_castling_valid):
        # Update the board with the new piece positions
        board.iloc[end_row, end_col] = piece
        board.iloc[start_row, start_col] = None

        # Print the updated board
        display_board(board)

    else:
        print("Invalid move. Please try again.")

def is_valid_move(board, move, player, can_castle=True):
    # Define dictionary of valid piece moves
    valid_moves = {'P': ['P+1'], 'p': ['p-1'], 'R': ['H', 'V'], 'r': ['h', 'v'],
                   'N': ['2H+1V', '1H+2V'], 'n': ['2h+1v', '1h+2v'],
                   'B': ['D'], 'b': ['d'], 'Q': ['D', 'H', 'V'], 'q': ['d', 'h', 'v'],
                   'K': ['1H', '1V', '1D'], 'k': ['1h', '1v', '1d']}
    
    # Parse the move into its current and destination square
    current_square, dest_square = move.split(',')
    
    # Convert the square notation to row and column indexes
    current_row, current_col = 8 - int(current_square[1]), ord(current_square[0]) - 97
    dest_row, dest_col = 8 - int(dest_square[1]), ord(dest_square[0]) - 97
    
    # Get the piece at the current square
    piece = board.iloc[current_row, current_col]

    if math.isnan(piece):
        return False

    # Check if the current player is moving their own piece
    if player == 'white' and piece.islower():
        return False
    elif player == 'black' and piece.isupper():
        return False
    
    # Check if the move is valid for the given piece
    valid_piece_moves = valid_moves.get(piece.upper(), [])
    move_direction = ''
    for direction in valid_piece_moves:
        if direction[0] in ('+', '-'):
            move_direction = direction[0]
            direction = direction[1:]
        if direction == 'H':
            if abs(current_row - dest_row) == 2 and abs(current_col - dest_col) == 1:
                return True
            elif abs(current_row - dest_row) == 1 and abs(current_col - dest_col) == 2:
                return True
        elif direction == 'V':
            if abs(current_row - dest_row) > 0 and current_col == dest_col:
                return True
            elif abs(current_col - dest_col) > 0 and current_row == dest_row:
                return True
        elif direction == 'D':
            if abs(current_row - dest_row) == abs(current_col - dest_col):
                return True
        else:
            raise ValueError(f"Invalid direction: {direction}")
    if move_direction == '+':
        return dest_row == current_row - 1 and dest_col == current_col
    elif move_direction == '-':
        return dest_row == current_row + 1 and dest_col == current_col
    return False

# Define the dictionary of piece symbols and their corresponding Unicode characters
PIECE_UNICODE = {'p': '♙', 'n': '♘', 'b': '♗', 'r': '♖', 'q': '♕', 'k': '♔',
                 'P': '♟', 'N': '♞', 'B': '♝', 'R': '♜', 'Q': '♛', 'K': '♚'}

# Modify the display_board function to use the dictionary to render the board
def display_board(board):
    print('    a b c d e f g h')
    print('  +------------------------+')
    for i in range(8):
        row = ' '.join(PIECE_UNICODE.get(str(board.iloc[i, j]), ' ') for j in range(8))
        print(f'{8 - i} | {row} | {8 - i}')
    print('  +------------------------+')
    print('    a b c d e f g h')

def is_game_over(board):
    """
    Check if the game is over by determining if there are any legal moves left for each player.
    Return True if the game is over, False otherwise.
    """
    for player in ["white", "black"]:
        for row in range(8):
            for col in range(8):
                piece = board.iloc[row, col]
                if piece != " " and piece.isupper() == (player == "white"):
                    for dest_row in range(8):
                        for dest_col in range(8):
                            dest_piece = board.iloc[dest_row, dest_col]
                            if is_valid_move(board, f"{chr(col+97)}{8-row},{chr(dest_col+97)}{8-dest_row}", player):
                                return False
    return True
