# default.py

import random

class DefaultPlayerStrategy:
    def __init__(self, token):
        self.token = token
        self.opponent_token = 'O' if token == 'X' else 'X'

    def select_move(self, game_state):
        available_moves = game_state.get_available_moves()
        
        # Attempt to win
        for move in available_moves:
            if self.can_win(game_state, move, self.token):
                return move
                
        # Block opponent's win
        for move in available_moves:
            if self.can_win(game_state, move, self.opponent_token):
                return move
                
        # Choose a strategic but not entirely random move
        strategic_move = self.select_strategic_move(available_moves)
        if strategic_move:
            return strategic_move
        
        # If no strategic move is identified, fallback to a random move
        return random.choice(available_moves)

    def can_win(self, game_state, move, token):
        game_state.apply_move(move, token)
        win = game_state.get_winner() == token
        game_state.undo_move(move)
        return win

    def select_strategic_move(self, available_moves):
        # Example of simple strategy: prefer edge positions over corners
        edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
        available_edges = [move for move in edges if move in available_moves]
        if available_edges:
            return random.choice(available_edges)
        return None
