import sys
sys.path.append('C/Users/Jason Blaisdell/Documents/GitHub/chess-game/Chess_Game')

from board import is_valid_move, create_board, move_piece, display_board, is_game_over
def play_game():
    # Initialize the game board
    board = create_board()

    # Set the initial player
    player = 'white'

    # Print the starting board position
    display_board(board)

    # Play the game
    while True:
        # Get the player's move
        move = input(f"{player.capitalize()} to move: ")
        
        # Check if the move is valid
        if not is_valid_move(board, move, player):
            print("Invalid move, try again.")
            continue
        
        # Move the piece
        board = move_piece(board, move, player)
        
        # Print the updated board position
        display_board(board)

        # Check if the game is over
        if is_game_over(board):
            print("Game over!")
            return

        # Switch the player
        if player == 'white':
            player = 'black'
        else:
            player = 'white'


play_game()
