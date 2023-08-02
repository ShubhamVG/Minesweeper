from random import sample
# from sys import setrecursionlimit
# setrecursionlimit(10**6)
from utils import EMPTY, MINE, POP, SAFE, MARKED, N_MINE_9

Default = -1
Grid = list[list[int]]

class Board:
    def __init__(self, size:int=9, n_mines:int=Default):
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
                if len(self.surrounding_cells(i)) == len(self.surrounding_cells(i, True)):
                    self.board_state[i] = POP

        print(self)


    def __repr__(self) -> str:
        str_repr = ""

        for row in self.get_board_state():
            str_repr += str(row) + "\n" 

        return str_repr

    
    def get_board_state(self) -> Grid:
        return [
            self.board_state[self.size*i : self.size*(i+1)] for i in range(self.size)
        ]
    

    def get_playable_board(self) -> Grid:
        return [
            self.playable_board[self.size*i : self.size*(i+1)] for i in range(self.size)
        ]
    

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
        

    def move(self, x:int = -1, y:int = -1, is_mark:bool = False, pos:int=-1) -> bool:
        """Makes a move and returns whether the move was made or not."""
        if pos == -1:
            pos = x + self.size * y

        try:
            # Right click
            if is_mark:
                if self.playable_board[pos] == EMPTY and self.flags_remaining > 0:
                    self.playable_board[pos] = MARKED
                    self.flags_remaining -= 1
                elif self.playable_board[pos] == MARKED:
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
                    # add pop too
        except IndexError as e:
            raise e
        
        return True
    

    def pop(self, pos:int):
        if len((cells := self.surrounding_cells(pos, only_visitable=True))) == 0:
            return
        
        for cell in cells:
            self.move(pos=cell)
            if self.board_state[pos] == SAFE:
                self.pop(cell)
    

    def surrounding_cells(self, pos:int, only_safe:bool = False, only_visitable:bool = False) -> list[int]:
        """`only_visitable` is a superset of `only_safe`."""
        cells = []
        size = self.size
        grid_size = size ** 2

        neighbor_indices = [
            -size-1, -size, -size+1,
            -1,                   1,
            size-1,   size,   size+1
        ]

        for neighbour_index in neighbor_indices:
            neighbor_pos = pos + neighbour_index

            if neighbor_pos < 0 or neighbor_pos >= grid_size:
                continue
            else:
                if only_safe:
                    if self.board_state[neighbor_pos] != MINE:
                        cells.append(neighbor_pos)
                if only_visitable:
                    if self.board_state[neighbor_pos] != MINE and self.playable_board[neighbor_pos] == EMPTY:
                        cells.append(neighbor_pos)
                else:
                    cells.append(neighbor_pos)

        return cells
    
if __name__ == "__main__":
    board = Board(10)
    print(board)
    x, y = int(input("Enter x: ")), int(input("Enter y: "))
    board.move(x, y)
    print(*board.get_playable_board())
    print(board)
    pos = int(input("Enter pos: "))
    print(board.surrounding_cells(pos, only_visitable=True))
    