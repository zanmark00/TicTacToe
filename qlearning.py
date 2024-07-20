# qlearning.py

import random
from board import Board
from game import GameState

class QLearningStrategy:
    def __init__(self, token, learning_rate=0.1, discount_factor=0.9, epsilon_decay_rate=0.995, min_exploration_rate=0.01, initial_q_value=0):
        self.token = token
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon_decay_rate = epsilon_decay_rate
        self.min_exploration_rate = min_exploration_rate
        self.exploration_rate = 1.0
        self.q_table = {}
        self.initial_q_value = initial_q_value

    def state_key(self, game_state):
        return str(game_state.board)

    def select_move(self, game_state):
        available_moves = game_state.get_available_moves()
        state_key = self.state_key(game_state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {move: self.initial_q_value for move in available_moves}
        if random.random() < self.exploration_rate:
            move = random.choice(available_moves)
        else:
            best_move = max(available_moves, key=lambda move: self.q_table[state_key].get(move, self.initial_q_value))
            move = best_move
        return move

    def update_q_table(self, state, action, reward, next_state, done):
        state_key = self.state_key(state)
        next_state_key = self.state_key(next_state) if next_state is not None else state_key
        next_max = 0 if done else max(self.q_table.get(next_state_key, {}).values(), default=self.initial_q_value)
        self.q_table[state_key][action] = (1 - self.learning_rate) * self.q_table[state_key].get(action, self.initial_q_value) + \
                                          self.learning_rate * (reward + self.discount_factor * next_max)

    def get_reward(self, game_state, winner):
        if winner == self.token:
            return 1.0
        elif winner is None and game_state.board.is_full():
            return 0.0
        else:
            return -1.0

    def train(self, player_manager, opponent_type, training_episodes):
        for episode in range(training_episodes):
            game_state = GameState(Board(), self, player_manager.create_player(opponent_type, 'O'))
            while not game_state.is_game_over():
                move = self.select_move(game_state)
                game_state.apply_move(move, self.token)
                
                reward = self.get_reward(game_state, game_state.get_winner())
                next_state = None if game_state.is_game_over() else game_state
                self.update_q_table(game_state, move, reward, next_state, game_state.is_game_over())
                
                if not game_state.is_game_over():
                    opponent_move = game_state.current_player.select_move(game_state)
                    game_state.apply_move(opponent_move, game_state.current_player.get_token())
            
            self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.epsilon_decay_rate)
