
PLAYERS = ["Nobody", "X", "O"]   # Two players, "X" and "O"
board = [0, 0, 0, # indices 0, 1, 2
        0, 0, 0, # indices 3, 4, 5
        0, 0, 0] # indices 6, 7, 8
player = 1  # X goes first
moves_left = 9  # number of moves so far 
winner = 0  # 0 means "nobody"

def display_board(board):
    '''display the current state of the board

    board layout:
    1 | 2 | 3
    4 | 5 | 6
    7 | 8 | 9

    Display numbers, unless a player has claimed a cell.
    Display player's mark if they have claimed the cell.
    Iterate through the board and choose the right thing
    to display for each cell

    Parameters
    ----------
    board: list
        the playing board
    '''

    board_to_show = "" # string that will display the board
    for i in range(len(board)):
        if board[i] == 0: # 0 means unoccupied
            # displayed numbers are one greater than the board index
            board_to_show += str(i + 1) # display cell number
        else:
            board_to_show += player_names[board[i]] # display player's mark
        if (i + 1) % 3 == 0: # every 3 cells, start a new row
            board_to_show += "\n"
        else:
            board_to_show += " | " # within a row, divide the cells
    print()
    print(board_to_show)


# while(moves_left > 0 and winner == 0):
display_board(board)
#    make_move()
 #   winner = check_win()
  #  player = 2 if (player == 1) else 1
  #  moves_left -= 1