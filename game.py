import time
from player import HumanPlayer, RandomComputerPlayer, SmartComputerPlayer

class TicTacToe:
    def __init__(self):
        self.board = self.make_board() # use a list to represent 3x3 board
        self.current_winner = None # keep track of the winner (aka who's turn it is; winner is always the one moving)

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        # print the tictactoe board
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]: 
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc (tells us what number corresponds to what box)
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' '] # this one-line is the same as the code below
        # moves = []
        # for (i, spot) in enumerate(self.board):
        #     # ['x', 'x', 'o'] --> [(0, 'x'), (1, 'x'), (2, 'o')]
        #     if spot == ' ':
        #         moves.append(i)
        # return moves

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        # check rows
        row_ind = square // 3 # 0, 1, 2 first row (= 0), 3, 4, 5 second (= 1), 6, 7, 8 third (= 2)
        row = self.board[row_ind*3 : (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True
        
        # check columns
        col_ind = square % 3 # 0, 3, 6 first column (= 0), 1, 4, 7 second (= 1), 2, 5, 8 third (= 2)
        column = [self.board[col_ind + i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # check diagonals
        if square % 2 == 0: # diagonal spots are 0, 2, 4, 6, 8 (even #s)
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal1]):
                return True
            if all([spot == letter for spot in diagonal2]):
                return True
        
        # otherwise no winner
        return False
    
def play(game, x_player, o_player, print_game = True, humans_only = True):
    if (print_game):
        game.print_board_nums()
    
    letter = 'X' # starting letter

    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        
        if game.make_move(square, letter):
            if print_game:
                print(letter + f' moved on square {square}')
                game.print_board()
                print('') # empty line

            if game.current_winner:
                if print_game:
                    print(letter + ' won the game.\n')
                return letter    

            # then alternate players
            letter = 'O' if letter == 'X' else 'X'

            # make it look smoother when playing against computer
            if print_game and not humans_only:
                time.sleep(1)
        
    if print_game:
        print('Game ended in draw.')

# Main function (runs the program)
if __name__ == '__main__':
    first_run = True # fr tho why does python not just have a do-while loop
    user_choice = ''
    while user_choice is not 'Q' or first_run is not True:
        print('Choose one of the following program functions:\n'
                + '         (A: Human vs. Human),\n'
                + '         (B: Human vs. RandomComputerPlayer),\n'
                + '         (C: Human vs. SmartComputerPlayer),\n'
                + '         (D: SmartComputerPlayer vs. RandomComputerPlayer)\n'
                + '         (Q: Quit the program)')
        user_choice = input().capitalize()
        if user_choice == 'A':
            x_player = HumanPlayer('X')
            o_player = HumanPlayer('O')
            t = TicTacToe()
            play(t, x_player, o_player, True, True)
        elif user_choice == 'B':
            x_player = HumanPlayer('X')
            o_player = RandomComputerPlayer('O')
            t = TicTacToe()
            play(t, x_player, o_player, True, False)
        elif user_choice == 'C':
            x_player = HumanPlayer('X')
            o_player = SmartComputerPlayer('O')
            t = TicTacToe()
            play(t, x_player, o_player, True, False)
        elif user_choice == 'D':
            x_wins = 0
            o_wins = 0
            ties = 0
            iterations = int(input('Number of times to run simulation: '))
            for run in range(iterations):
                x_player = RandomComputerPlayer('X')
                o_player = SmartComputerPlayer('O')
                t = TicTacToe()
                result = play(t, x_player, o_player, False, False)
                if result == 'X':
                    x_wins += 1
                elif result == 'O':
                    o_wins += 1
                else:
                    ties += 1
                if run % 5 == 0:
                    print(f'Running {run} times...')
            print('\nOverall result:\n'
                + f'Total # of games played: {iterations}\n'
                + f'X (RandomComputerPlayer) wins: {x_wins}\n'
                + f'O (SmartComputerPlayer) wins: {o_wins}\n'
                + f'Ties: {ties}\n')
        elif user_choice == 'Q':
            print('Quitting the program.')
            break
        else:
            print('Not a valid input.\n')
        first_run = False
