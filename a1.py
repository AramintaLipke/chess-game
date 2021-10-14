
"""
Chess Game
Assignment 1
Semester 2, 2021
CSSE1001/CSSE7030
"""

from typing import Optional, Tuple

from a1_support import *

# Replace these <strings> with your name, student number and email address.
__author__ = "Araminta Lipke, 45807424"
__email__ = "a.lipke@uq.net.au"


def initial_state() -> Board:
    """Returns the game board as it would be set up for White to make the first
        move of the game.

    Returns:
        tuple(str, str, str, str, str, str, str, str): The eight rows of the
        chess board as strings.
    """
    board = ("rnbqkbnr", "pppppppp", "........", "........", "........",
             "........", "PPPPPPPP", "RNBQKBNR")

    return board


def print_board(board: Board) -> None:
    """Prints the game boad in a readable format for the user with the row letters
        and column numbers.

    Parameters:
        board (Board): The current board state.
    """
    for i in range(len(board)):
        print(f"{board[i]}  {len(board)-i}")
    
    print('')
    print('abcdefgh')


def square_to_position(square: str) -> Position:
    """Converts the chess notation into its (row, col): Position equivelant.

    Parameters:
        square (str): a chess notation in its raw string format.

    Returns:
        (Position): The (row, col) position.
    """
    letters = 'abcdefgh'
    position = list((0, 0))
    
    for i in range(len(letters)):
        if letters[i] == square[0]:
            position[1] = i

    for i in range(BOARD_SIZE):
        if int(square[1]) == i:
            position[0] = BOARD_SIZE - i

    position = tuple(position)
            
    return position


def process_move(user_input: str) -> Move:
    """Converts the raw user input into its ((Position), (Position)): Move
        equivelant.

    Parameters:
        user_input (str): The raw input from the user.
        
    Returns:
        (Move): The ((Position), (Position)) move.
        
    """    
    move = list(((0, 0), (0, 0)))

    move[0] = square_to_position(user_input[0:2])
    move[1] = square_to_position(user_input[3:5])

    move = tuple(move)

    return move 
    

def change_position(board: Board, position: Position, character: str) -> Board:
    """Returns a copy of the board with the character at the position changed to
        the character.

    Parameters:
        board (Board): The current board state.
        position (Position): The (row, col) position.
        character (str): The character that will be moved to the position.

    Returns:
        (Board): The new board state with the character in the old and new
                    position.
    """
    board = list(board)
    
    row = board[position[0]]
    new_row = row[:position[-1]] + character + row[position[-1] + 1:]
    board[position[0]] = new_row

    board = tuple(board)    

    return board


def clear_position(board: Board, position: Position) -> Board:
    """Replaces the position of the character moved with a '.'. indicating an empy
        space.

    Parameters:
        board (Board): The current state of the board.
        position (Position): The (row, col) position.

    Returns:
        (Board): The new board state with the character at position replaced.
    """
    board = list(board)
    
    row = board[position[0]]
    new_row = row[:position[-1]] + '.' + row[position[-1] + 1:]
    board[position[0]] = new_row

    board = tuple(board)    
    return board
    

def update_board(board: Board, move: Move) -> Board:
    """
    Returns the updated board with the move made.

    Parameters:
        board (Board): The current board state.
        move (Move): The (Position, Position) move.

    Returns:
        (Board): The updated board after the move has been made.
    """
    old_position = move[0]
    new_position = move[1]
    character = board[old_position[0]][old_position[1]]
    board = change_position(board, new_position, character)
    board = clear_position(board, old_position)
    
    return board


def is_current_players_piece(piece: str, white_turn: bool) -> bool:
    """Determines if the player whos turn it is, owns the piece.

    Parameters:
        piece (str): The character being tested.
        whites_turn (bool): True iff it's whites turn.

    Returns:
    (bool): True iff the piece belongs to the player whose turn it is.
    """
    if white_turn and piece in WHITE_PIECES:
        return True
    elif not white_turn and piece in BLACK_PIECES:
        return True
    else:
        return False


def is_move_valid(move: Move, board: Board, whites_turn: bool) -> bool:
    """Returns True iff all conditions are met for the move to be valid.

    Parameters:
        move (Move): The (Position, Position) move.
        board (Board): The current state of the board.
        whites_turn (bool): True iff it's white's turn.

    Returns:
        (bool): True iff the move is valid.
    """
    if out_of_bounds(move[0]) == True or out_of_bounds(move[1]) == True:
        return False
    
    if move[0] == move[1]:
        return False

    if is_current_players_piece(piece_at_position(move[0], board), False) and whites_turn == True:
        return False
    elif is_current_players_piece(piece_at_position(move[0], board), True) and whites_turn == False:
        return False


    if piece_at_position(move[1], board) in WHITE_PIECES and whites_turn == True:
        return False
    elif piece_at_position(move[1], board) in BLACK_PIECES and whites_turn == False:
        return False


    if move[1] not in get_possible_moves(move[0], board):
        return False


    test_board = board
    test_board = update_board(test_board, move)
    if is_in_check(test_board, True) and whites_turn == True:
        return False
    elif is_in_check(test_board, False) and whites_turn == False:
        return False

    return True


def can_move(board: Board, whites_turn: bool) -> bool:
    """Returns True if the player whose turn just started can make a valid move
        without entering check.

    Parameters:
        board (Board): The current state of the board.
        whites_turn (bool): Ture iff it's white's turn.

    Returns:
        (bool): True iff a valid move can be made without entering check.
    """
    friendly_pieces = WHITE_PIECES if whites_turn else BLACK_PIECES
    temp_board = board

    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            position = (i, j)

            if piece in friendly_pieces:
                new_positions = get_possible_moves(position, board)

                for new_pos in new_positions:
                    temp_board = change_position(board, new_pos, piece)
                    temp_board = clear_position(temp_board, position)

                    if not is_in_check(temp_board, whites_turn):
                        return True

    return False
                

def is_stalemate(board: Board, whites_turn: bool) -> bool:
    """Returns True iff a stalemate has been reached.

    Parameters:
        board (Board): The current state of the board.
        whites_turn (bool): True iff it's white's turn.

    Returns:
        (bool): True iff a stalemate has been reached.
    """
    if not can_move(board, whites_turn) and not is_in_check(board, whites_turn):
        return True
    else:
        return False


def check_game_over(board: Board, whites_turn: bool) -> bool:
    """Returns True if either checkmate or stalemate has been reached to
        indicate the end of the game. Prints reason for game end.

    Parameters:
        board (Board): The current state of the board.
        whites_turn (bool): True iff it's white's turn.

    Returns:
        (bool): True iff the game is over.
    """
    if is_in_check(board, whites_turn) and can_move(board, whites_turn):
        turn = 'White' if whites_turn else 'Black'
        print()
        print(f'{turn} is in check')
        return False
    elif is_in_check(board, whites_turn) and can_move(board, whites_turn) == False:
        print()
        print('Checkmate')
        return True
    elif is_stalemate(board, whites_turn):
        print()
        print('Stalemate')
        return True
    else:
        return False
        

def main():
    """Entry point to gameplay"""
    
    is_white_move = True
    board = initial_state()
    print_board(board)
    
    while True:
        if is_white_move == True:
            print()
            result = str(input("White's move: "))
        else:
            print()
            result = str(input("Black's move: "))

        if result == 'h' or result == 'H':
            print(HELP_MESSAGE)
            print_board(board)
        elif result == 'q' or result == 'Q':
            confirm_quit = str(input("Are you sure you want to quit? "))
            if confirm_quit == 'y' or confirm_quit == "Y":
                break
            else:
                print_board(board)            

        else:
            if valid_move_format(result) == False:
                print('Invalid move')
                print()
                print_board(board)
            else:
                move = process_move(result)
                if is_move_valid(move, board, is_white_move):                
                    board = update_board(board, move)
                    print_board(board)
                    is_white_move = not is_white_move
                    if check_game_over(board, is_white_move):
                        break
                else:
                    print('Invalid move')
                    print()
                    print_board(board)
                
if __name__ == "__main__":
    main()
