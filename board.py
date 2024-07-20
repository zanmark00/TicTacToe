# board.py

class Board:
    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.board = [[None] * cols for _ in range(rows)]
        self.available_moves = [(r, c) for r in range(rows) for c in range(cols)]

    def reset(self):
        self.board = [[None] * self.cols for _ in range(self.rows)]
        self.available_moves = [(r, c) for r in range(self.rows) for c in range(self.cols)]

    def get_state(self):
        return [row[:] for row in self.board]

    def get_winner(self):
        for row in self.board:
            if len(set(row)) == 1 and row[0] is not None:
                return row[0]
        for col in range(self.cols):
            column = [self.board[row][col] for row in range(self.rows)]
            if len(set(column)) == 1 and column[0] is not None:
                return column[0]
        diagonal1 = [self.board[i][i] for i in range(self.rows)]
        if len(set(diagonal1)) == 1 and diagonal1[0] is not None:
            return diagonal1[0]
        diagonal2 = [self.board[i][self.cols - i - 1] for i in range(self.rows)]
        if len(set(diagonal2)) == 1 and diagonal2[0] is not None:
            return diagonal2[0]
        return None

    def get_available_moves(self):
        return self.available_moves[:]

    def make_move(self, action, player_token):
        if isinstance(action, tuple) and len(action) == 2:
            row, col = action
            if 0 <= row < self.rows and 0 <= col < self.cols and self.board[row][col] is None:
                self.board[row][col] = player_token
                self.available_moves.remove(action)
            else:
                raise ValueError("Move not valid")
        else:
            raise ValueError("Invalid move format")

    def is_full(self):
        return len(self.available_moves) == 0

    def print_board(self):
        for i, row in enumerate(self.board):
            print(' | '.join([cell if cell is not None else ' ' for cell in row]))
            if i < self.rows - 1:
                print('-' * (self.cols * 4 - 1))
