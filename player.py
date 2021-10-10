import math
import random

class Player:
    def __init__(self, letter):
        # letter is X or O
        self.letter = letter

    def get_move(self, game):
        pass

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8): ')
            print('')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.\n')
        return val

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

# this is *technically* an AI program (uses a minimax algorithm)
# minimax algorithm (from my understanding):
# 1. the program calculates all possible moves & assigns a value to each end game state
# 2. it then assigns that value to the moves leading up to that game state and makes decisions based on those values;
# 3. the program chooses the value that maximizes their own game state and minimizes the enemy game state
# so this program's minimax algorithm (utility function) is ((1 or -1 depending on winner) * (# of empty squares + 1)) 
class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9: # if first move, then randomly choose
            square = random.choice(game.available_moves())
        else: # otherwise use minimax algorithm to find next best move
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter # the SmartComputerPlayer
        mini_player = 'O' if player == 'X' else 'X' # the player it's against

        if state.current_winner == mini_player:
            return {'position': None,
                    # positive 1 for SmartComputerPlayer wins, negative 1 otherwise
                    'score': 1 * (state.num_empty_squares() + 1) if mini_player == max_player 
                        else -1 * (state.num_empty_squares() + 1)
            }
        elif not state.empty_squares():
            return {'position': None,
                    'score': 0
            }
        
        # placeholder dictionaries that hold the highest possible values (infinity & negative infinity)
        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            # step 1: make move
            state.make_move(possible_move, player)
            # step 2: simulate game after making move
            sim_score = self.minimax(state, mini_player)

            # step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move 
            # step 4: update dictionaries (if simulation one leads to better outcome)
            if player == max_player: # maximize the max_player (SmartComputerPlayer)
                if sim_score['score'] > best['score']:
                    best = sim_score
            else: # minimize the other player
                if sim_score['score'] < best['score']:
                    best = sim_score
        
        return best
