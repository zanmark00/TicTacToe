# game.py

from board import Board

class GameState:
    def __init__(self, board, player1, player2):
        self.board = board
        self.current_player = player1
        self.player1 = player1
        self.player2 = player2

    def get_available_moves(self):
        return self.board.get_available_moves()

    def apply_move(self, move, token):
        self.board.make_move(move, token)
        self.current_player = self.get_next_player()

    def undo_move(self, move):
        row, col = move
        self.board.board[row][col] = None
        self.board.available_moves.append(move)
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def is_game_over(self):
        return self.board.is_full() or self.board.get_winner() is not None

    def get_winner(self):
        return self.board.get_winner()

    def get_state_key(self):
        return tuple(tuple(row) for row in self.board.board)

    def get_next_player(self):
        return self.player2 if self.current_player == self.player1 else self.player1

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.game_state = GameState(self.board, player1, player2)

    def play(self):
        while not self.game_state.is_game_over():
            current_player = self.game_state.current_player
            move = current_player.select_move(self.game_state)
            
            if move:
                self.game_state.apply_move(move, current_player.get_token())
                self.board.print_board()
                print()

                if self.game_state.get_winner():
                    print(f"{self.game_state.get_winner()} wins!")
                    break
            else:
                print(f"No valid move available for {current_player.get_token()}. It's a tie!")
                break
            
        if not self.game_state.get_winner():
            print("It's a tie!")
