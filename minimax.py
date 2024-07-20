import math


class MinimaxStrategy():
    def __init__(self, token, use_alpha_beta=True):
        self.token = token
        self.opponent_token = 'O' if token == 'X' else 'X'
        self.use_alpha_beta = use_alpha_beta

    def select_move(self, game_state):
        _, best_move = self.minimax(game_state, float('-inf'), float('inf'), True) if self.use_alpha_beta else self.minimax_no_pruning(game_state, True)
        return best_move

    def minimax(self, game_state, alpha, beta, maximizing_player):
        if game_state.is_game_over():
            return self.evaluate(game_state), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in game_state.get_available_moves():
                game_state.apply_move(move, self.token)
                eval, _ = self.minimax(game_state, alpha, beta, False)
                game_state.undo_move(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in game_state.get_available_moves():
                game_state.apply_move(move, self.opponent_token)
                eval, _ = self.minimax(game_state, alpha, beta, True)
                game_state.undo_move(move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def minimax_no_pruning(self, game_state, maximizing_player):
        if game_state.is_game_over():
            return self.evaluate(game_state), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in game_state.get_available_moves():
                game_state.apply_move(move, self.token)
                eval, _ = self.minimax_no_pruning(game_state, False)
                game_state.undo_move(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in game_state.get_available_moves():
                game_state.apply_move(move, self.opponent_token)
                eval, _ = self.minimax_no_pruning(game_state, True)
                game_state.undo_move(move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def evaluate(self, game_state):
        winner = game_state.get_winner()
        if winner == self.token:
            return math.inf
        elif winner == self.opponent_token:
            return -math.inf
        else:
            return 0
