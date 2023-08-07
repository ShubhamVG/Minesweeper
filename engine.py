from board import Board
from click import clear
from winsound import Beep
from board import Board
from utils import SAFE, EMPTY, MINE, N_MINE_1, N_MINE_8, FLAG
from numpy import matrix
from random import choice

FlattenedBoard = list[int]

class Engine:
    """Engine needs the `playable_board` from of the `Board`."""

    def __init__(self, board: FlattenedBoard, n_mines: int) -> None:
        self.board = board
        self.mines_remaining = n_mines
        self.flags_remaining = n_mines
        self.size = len(board)
        self.evaluation_board = [n_mines/self.size for _ in range(self.size)]


class Childe(Engine):
    """First engine and failed one."""

    def __init__(self, board: FlattenedBoard, n_mines: int):
        print("Warning: Childe does not work as intended.")

        super().__init__(board, n_mines)
        self.update_evaluation()


    def best_move(self) -> (int, bool):
        min_value = min(self.evaluation_board, key=lambda x: x if x is not None else 100)
        max_val = max(self.evaluation_board, key=lambda x: x if x is not None else -100)

        if max_val >= 1:
            pos = self.evaluation_board.index(max_val)
            surrounding_cells_pos = self.__surrounding_cells(pos)

            for cell_pos in surrounding_cells_pos:
                if self.evaluation_board[cell_pos] >= N_MINE_1 and self.evaluation_board[cell_pos] <= N_MINE_8:
                    self.evaluation_board[cell_pos] -= 1
            
            return pos, True

        return self.evaluation_board.index(min_value), False
    

    def __get_n_mines_pos(self) -> set[int]:
        """Returns the positions of only those squares where `N_MINE_X` is present."""

        cells = set()
        
        for pos in range(self.size):
            if self.board[pos] >= N_MINE_1 and self.board[pos] <= N_MINE_8:
                cells.add(pos)
            
        return cells


    def __surrounding_cells(self, pos: int, only_visitable: bool = True) -> set[int]:
        cells = set()
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
                        cells.add(neighbor_pos)
                else:
                    cells.add(neighbor_pos)
        
        return cells

    
    def update_board(self, board: FlattenedBoard, has_lost: bool):
        self.board = board

        if has_lost:
            self.best_move = lambda: print("Already lost :p")

    
    def update_evaluation(self):
        self.evaluation_board = [0.0 for _ in range(self.size)]
        possible_mines_count = 0
        n_mines_pos = self.__get_n_mines_pos()

        for pos in n_mines_pos:
            n_mine_val = self.board[pos]
            possible_mines_count += n_mine_val
            surrounding_cells = self.__surrounding_cells(pos)
            n_cells = len(surrounding_cells)

            for cell in surrounding_cells:
                self.evaluation_board[cell] = self.evaluation_board[cell] if self.evaluation_board[cell] > n_mine_val/n_cells else n_mine_val/n_cells
            
        remaining_mines = self.mines_remaining - possible_mines_count
        p_zero_cells_count = self.evaluation_board.count(0.0)

        for cell in range(self.size):
            if self.board[cell] == EMPTY:
                if self.evaluation_board[cell] == 0:
                    self.evaluation_board[cell] = remaining_mines/p_zero_cells_count
            else:
                self.evaluation_board[cell] = None


class Thoma(Engine):
    """Second Engine. The one which kinda works."""

    def __init__(self, board: FlattenedBoard, n_mines: int) -> None:
        super().__init__(board, n_mines)

    
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
                    elif self.evaluation_board[cell] > n_mine_val/n_cells and self.evaluation_board[cell] > 0:
                        self.evaluation_board[cell] = n_mine_val/n_cells

        p_zero_cells_count = self.evaluation_board.count(None)
        
        for cell in range(self.size):
            if self.board[cell] == EMPTY:
                if self.evaluation_board[cell] == None:
                    self.evaluation_board[cell] = self.mines_remaining/p_zero_cells_count
