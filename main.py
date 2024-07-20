# main.py

import time
from players import PlayerManager
from game import Game
from qlearning import QLearningStrategy

def create_player(player_manager, player_type, token, training_iterations=None):
    learning_rate = 0.1
    discount_factor = 0.9
    epsilon_decay_rate = 0.999
    min_exploration_rate = 0.01
    max_episodes = 500000 if training_iterations is None else training_iterations
    
    if player_type == 'qlearning':
        start_time = time.time()  
        player = player_manager.create_player(player_type, token, learning_rate=learning_rate, discount_factor=discount_factor, epsilon_decay_rate=epsilon_decay_rate, min_exploration_rate=min_exploration_rate, max_episodes=max_episodes)
        opponent_type = 'default'
        player.strategy.train(player_manager, opponent_type, max_episodes)
        end_time = time.time()  
        print(f"Training time for player {token}: {end_time - start_time:.2f} seconds.")
    elif player_type == 'minimax':
        use_alpha_beta = input("Use alpha-beta pruning? (y/n): ").strip().lower() == 'y'
        player = player_manager.create_player(player_type, token, use_alpha_beta=use_alpha_beta)
    else:
        player = player_manager.create_player('default', token)
    
    return player

def run_iterations(player1, player2, num_iterations):
    results = {'X': {'wins': 0, 'losses': 0}, 'O': {'wins': 0, 'losses': 0}, 'draws': {'total': 0}}
    for _ in range(num_iterations):
        game = Game(player1, player2)
        game.play()
        winner = game.game_state.get_winner()
        if winner is None:
            results['draws']['total'] += 1
        else:
            results[winner]['wins'] += 1
            loser = 'O' if winner == 'X' else 'X'
            results[loser]['losses'] += 1
    
    return results

def main():
    player_manager = PlayerManager()
    
    for player_number in [1, 2]:
        print(f"Select player {player_number} strategy ('minimax', 'qlearning', 'default'):")
        player_type = input().strip().lower()
        
        training_iterations = None
        if player_type == 'qlearning':
            print(f"Enter the number of training iterations for player {player_number}:")
            training_iterations = int(input())
        
        if player_number == 1:
            player1 = create_player(player_manager, player_type, 'X', training_iterations=training_iterations)
        else:
            player2 = create_player(player_manager, player_type, 'O', training_iterations=training_iterations)
    
    print("Enter the number of game iterations to play:")
    num_iterations = int(input())
    results = run_iterations(player1, player2, num_iterations)
    
    print("\nResults:")
    for token in ['X', 'O']:
        stats = results[token]
        draws = results['draws']['total']
        print(f"Player {token}: Wins: {stats['wins']}, Losses: {stats['losses']}, Draws: {draws}")

if __name__ == "__main__":
    main()
