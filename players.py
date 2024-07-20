# players.py

import abc
import random

class Player(abc.ABC):
    def __init__(self, token):
        self.token = token

    @abc.abstractmethod
    def get_strategy(self):
        pass

    def get_token(self):
        return self.token

class AIPlayer(Player):
    def __init__(self, token, strategy):
        super().__init__(token)
        self.strategy = strategy

    def get_strategy(self):
        return self.strategy

    def select_move(self, game_state):
        return self.strategy.select_move(game_state)

class MinimaxPlayer(AIPlayer):
    def __init__(self, token, use_alpha_beta=True):
        from minimax import MinimaxStrategy
        strategy = MinimaxStrategy(token, use_alpha_beta)
        super().__init__(token, strategy)

class QLearningPlayer(AIPlayer):
    def __init__(self, token, learning_rate, discount_factor, epsilon_decay_rate, min_exploration_rate, max_episodes):
        from qlearning import QLearningStrategy
        strategy = QLearningStrategy(token, learning_rate, discount_factor, epsilon_decay_rate, min_exploration_rate, max_episodes)
        super().__init__(token, strategy)

class DefaultPlayer(AIPlayer):
    def __init__(self, token):
        from default import DefaultPlayerStrategy
        strategy = DefaultPlayerStrategy(token)
        super().__init__(token, strategy)

class PlayerManager:
    def __init__(self):
        self.player_classes = {
            'minimax': MinimaxPlayer,
            'qlearning': QLearningPlayer,
            'default': DefaultPlayer,
        }

    def create_player(self, player_type, token, **kwargs):
        if player_type in self.player_classes:
            player_class = self.player_classes[player_type]
            player_args = kwargs.copy()
            player_args['token'] = token
            return player_class(**player_args)
        else:
            raise ValueError(f"Invalid player type: {player_type}")