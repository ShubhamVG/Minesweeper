from random import sample
from utils import EMPTY, MINE, POP, SAFE, FLAG
from numpy import matrix
from sys import setrecursionlimit
setrecursionlimit(10**6)

Default = -1
Grid = list[list[int]]

class Board:
    def __init__(self, size: int = 9, n_mines: int = Default):
        if n_mines == Default:
            n_mines = size ** 2 // 4

        grid_size = size ** 2
        mine_positions = sample(range(grid_size), n_mines)

        self.size = size
        self.flags_remaining = n_mines
        self.playable_board = [EMPTY for _ in range(grid_size)]
        self.board_state = [MINE if i in mine_positions else SAFE for i in range(grid_size)]

        for pos in mine_positions:
            neighbor_cells = self.surrounding_cells(pos, only_safe=True)

            for neighbor_cell in neighbor_cells:
                self.board_state[neighbor_cell] += 1

        for i in range(grid_size):
            if self.board_state[i] == SAFE:
                if len(self.surrounding_cells(i)) == len(self.surrounding_cells(i, only_safe=True)):
                    self.board_state[i] = POP


    def __repr__(self) -> str:
        return str(self.get_board_state())

    
    def get_board_state(self) -> Grid:
        return matrix([
            self.board_state[self.size*i : self.size*(i+1)] for i in range(self.size)
        ])
    

    def get_playable_board(self) -> Grid:
        return matrix([
            self.playable_board[self.size*i : self.size*(i+1)] for i in range(self.size)
        ])
    

    def has_lost(self) -> bool:
        if MINE in self.playable_board:
            return True

        return False
    

    def has_won(self) -> bool:
        if (not self.has_lost()) and (EMPTY not in self.playable_board):
            return True
        
        return False
    

    def is_gameover(self) -> bool:
        if self.has_lost() or self.has_won():
            return True
        
        return False
        

    def move(self, pos: int, is_flag: bool = False) -> bool:
        """Makes a move and returns whether the move was made or not."""

        try:
            # Right click
            if is_flag:
                if self.playable_board[pos] == EMPTY and self.flags_remaining > 0:
                    self.playable_board[pos] = FLAG
                    self.flags_remaining -= 1
                elif self.playable_board[pos] == FLAG:
                    self.playable_board[pos] = EMPTY
                    self.flags_remaining += 1
                else:
                    return False
            # Normal click
            else:
                if self.playable_board[pos] == EMPTY:
                    self.playable_board[pos] = self.board_state[pos]

                    if self.playable_board[pos] == POP:
                        self.playable_board[pos] = SAFE
                        self.pop(pos)
                else:
                    return False
        except IndexError as e:
            raise e
        
        return True
    

    def pop(self, pos: int):
        if len((cells := self.surrounding_cells(pos, only_visitable=True))) == 0:
            return
        
        for cell in cells:
            self.move(pos=cell)
            if self.board_state[pos] == SAFE:
                self.pop(cell)
    

    def surrounding_cells(self, pos: int, only_safe: bool = False, only_visitable: bool = False) -> set[int]:
        """`only_visitable` is a superset of `only_safe`."""

        cells = set()
        size = self.size

        neighbor_indices = [
            (-1, -1), (-1, 0), (-1, 1),
            (0,  -1),          (0,  1),
            (1,  -1), (1,  0), (1,  1)
        ]

        for neighbour_index in neighbor_indices:
            x = pos % size + neighbour_index[0]
            y = pos // size + neighbour_index[1]

            if any([coord < 0 or coord >= size for coord in (x, y)]):
                continue
            else:
                neighbor_pos = x + y*size
                
                if only_safe:
                    if self.board_state[neighbor_pos] != MINE:
                        cells.add(neighbor_pos)
                elif only_visitable:
                    if self.board_state[neighbor_pos] != MINE and self.playable_board[neighbor_pos] == EMPTY:
                        cells.add(neighbor_pos)
                else:
                    cells.add(neighbor_pos)

        return cells