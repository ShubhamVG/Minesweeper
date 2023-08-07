from board import Board
from game import choose_option, run_game

grid_size = choose_option() + 9 #+9 because of grid_size returns [0-2]
board = Board(grid_size)
run_game(board)
