from board import Board
from game import choose_option, run_game

grid_len, use_engine = choose_option()
board = Board(grid_len, 16)
run_game(board, use_engine)