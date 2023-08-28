from utils import EMPTY, N_MINE_1, N_MINE_8, FLAG
from random import choice

FlattenedBoard = list[int]

class Engine:
    """Engine needs the `playable_board` form of the `Board`."""

    def __init__(self, board: FlattenedBoard, n_mines: int) -> None:
        self.board = board
        self.mines_remaining = n_mines
        self.flags_remaining = n_mines
        self.size = len(board)
        self.evaluation_board = [n_mines/self.size for _ in range(self.size)]


    def best_move(self) -> (int, bool):
        min_val = min(self.evaluation_board, key=lambda x: x if x is not None else 100)

        if min_val == -1:
            self.mines_remaining -= 1
            self.flags_remaining -= 1

        return choice(self.__get_empty_squares_with_same_p(min_val)), min_val == -1


    def __get_empty_squares_with_same_p(self, p: int) -> list[int]:
        """Returns the positions of only those which have not been visited yet (`EMPTY`) with a given `p`."""

        cells = []

        for pos in range(self.size):
            if self.board[pos] == EMPTY and self.evaluation_board[pos] == p:
                cells.append(pos)

        return cells

    
    def __get_n_mines_pos(self) -> set[int]:
        """Returns the positions of only those squares where `N_MINE_X` is present."""

        cells = set()
        
        for pos in range(self.size):
            if self.board[pos] >= N_MINE_1 and self.board[pos] <= N_MINE_8:
                cells.add(pos)
            
        return cells
    
    
    def __surrounding_cells(self, pos: int, only_visitable: bool = True) -> list[int]:
        cells = []
        length = int(self.size ** 0.5)

        neighbor_indices = [
            (-1, -1), (-1, 0), (-1, 1),
            (0,  -1),          (0,  1),
            (1,  -1), (1,  0), (1,  1)
        ]

        for neighbour_index in neighbor_indices:
            x = pos % length + neighbour_index[0]
            y = pos // length + neighbour_index[1]
            neighbor_pos = x + y*length

            if any([coord < 0 or coord >= length for coord in (x, y)]):
                continue
            else:
                if only_visitable:
                    if self.board[neighbor_pos] == EMPTY:
                        cells.append(neighbor_pos)
                else:
                    cells.append(neighbor_pos)
        
        return cells


    def update_board(self, board: FlattenedBoard, has_lost: bool):
        self.board = board

        if has_lost:
            self.best_move = lambda: print("Already lost :p")

    
    def update_evaluation(self):
        self.evaluation_board = [None for _ in range(self.size)]
        n_mines_pos = self.__get_n_mines_pos()

        for pos in n_mines_pos:
            n_mine_val = self.board[pos]
            n_flags_marked = [
                1 if self.board[cell] == FLAG else 0 for cell in self.__surrounding_cells(pos, False)
            ].count(1)
            cells = self.__surrounding_cells(pos)

            if n_flags_marked == n_mine_val:
                for cell in cells:
                    self.evaluation_board[cell] = 0
            elif  len(cells) == n_mine_val - n_flags_marked:
                for cell in cells:
                    self.evaluation_board[cell] = -1
            else:
                n_mine_val -= n_flags_marked
                n_cells = len(cells)

                for cell in cells:
                    if self.evaluation_board[cell] == None:
                        self.evaluation_board[cell] = n_mine_val/n_cells
                    elif self.evaluation_board[cell] > 0:
                        self.evaluation_board[cell] += n_mine_val/n_cells

        p_zero_cells_count = self.evaluation_board.count(None)
        
        for cell in range(self.size):
            if self.board[cell] == EMPTY:
                if self.evaluation_board[cell] == None:
                    self.evaluation_board[cell] = self.mines_remaining/p_zero_cells_count