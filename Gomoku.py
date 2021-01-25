# Gomoku is Japanese name for the popular game - five in a row.
# Running python Gomoku.py will reveal the syntax for the program.
# Here is an example: python Gomoku.py computer Bot1 computer Bot2 9
import sys
import random
import time
from os import system

class Stone:
    """Stone class contains the type of the stone and allows for proper
    representation on the board.
    """

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        if self.color == 'black':
            return '●'
        elif self.color == 'white':
            return '◯'

class Board:
    """Board class contains board size and remembers all the stones that have
    been placed on the board. It also evaluates if a move is valid and if one
    side has won the game, and allows for proper representation of the board.
    """

    def __init__(self, size):
        self.size = size
        self.board = dict()
        self.pattern_pos = None

        # initialize an empty board
        for row in range(self.size):
                for col in range(self.size):
                    self.board[(row, col)] = None

    # return True if move is valid, False otherwise
    def eval_move(self, row, col):
        if row >= self.size or row < 0 or col >= self.size or col < 0:
            return False
        elif self.board[(row, col)] is not None:
            return False
        else:
            return True

    # check if there is five in a row/col/diagonally on the board
    # return the positions if there is, None otherwise.
    def eval_win(self):

        pattern = Pattern(board)

        pattern_pos = pattern.find_pattern_row(5)
        if(len(pattern_pos['black'])>0 or len(pattern_pos['white'])>0):
            return pattern_pos

        pattern_pos = pattern.find_pattern_col(5)
        if(len(pattern_pos['black'])>0 or len(pattern_pos['white'])>0):
            return pattern_pos

        pattern_pos = pattern.find_pattern_diag1(5)
        if(len(pattern_pos['black'])>0 or len(pattern_pos['white'])>0):
            return pattern_pos

        pattern_pos = pattern.find_pattern_diag2(5)
        if(len(pattern_pos['black'])>0 or len(pattern_pos['white'])>0):
            return pattern_pos

        return None

    def __repr__(self):
        board_string = '   '

        for col in range(self.size):
            # ensure proper alignment
            if col+1 < 10:
                board_string += str(col+1) + '  '
            else:
                board_string += str(col+1) + ' '
        board_string += '\n'

        for row in range(self.size):
            if row+1 <10:
                board_string += str(row+1) + '  '
            else:
                board_string += str(row+1) + ' '

            for col in range(self.size):
                if self.board[(row, col)] is None:
                    board_string += '·  '
                else:
                    if self.pattern_pos is None:
                        board_string += str(self.board[(row, col)])
                        board_string += '  '
                    else:
                        pattern_pos = self.pattern_pos['black'] + self.pattern_pos['white']
                        if (row, col) in pattern_pos[0]:
                            # colorama code for coloring the stone in red
                            board_string += '\033[31m'
                            board_string += str(self.board[(row, col)])
                            board_string += '\033[39m'
                            board_string += '  '
                        else:
                            board_string += str(self.board[(row, col)])
                            board_string += '  '

            board_string += '\n'

        return board_string

class Pattern:
    """Pattern is class for checking patterns. Currently implemented patterns
    include n in a row/col/diagonally. Potential other patterns inculde
    evaluating sequences with gaps inside, as well as checking liberties on
    both sides of the sequence.
    """
    def __init__(self, board):
        self.board = board

    def find_pattern_row(self, n):

        stone = None
        counter = 0
        pos = []
        pattern_position = {'black':[], 'white':[]}

        for row in range(self.board.size):
            for col in range(self.board.size):
                if self.board.board[(row, col)] is None:
                    counter = 0
                    pos = []
                    next
                else:
                    if self.board.board[(row, col)] == stone:
                        # same stone as the previous one
                        counter +=1
                        pos.append((row, col))
                        if counter == n:
                            pattern_position[stone.color].append(pos.copy())
                            counter = 0
                            pos = []
                    else:  # different stone from previous stone
                        counter = 1
                        pos = [(row, col)]
                        stone = self.board.board[(row, col)]
            counter = 0
            pos = []
            stone = None

        return pattern_position

    def find_pattern_diag1(self, n):
        stone = None
        counter = 0
        pos = []
        pattern_position = {'black':[], 'white':[]}

        # looping matrix diagonally is tricky algebraically
        # the method I used referenced athe following stackoverflow post.
        # https://stackoverflow.com/questions/20420065/loop-diagonally-through-two-dimensional-array
        for k in range(self.board.size*2):
            for j in range(k+1):
                i = k - j
                if i < self.board.size and j < self.board.size:
                    if self.board.board[(i, j)] is None:
                        counter = 0
                        pos = []
                        next
                    else:
                        if self.board.board[(i, j)] == stone:
                            counter += 1
                            pos.append((i, j))
                            if counter == n:
                                pattern_position[stone.color].append(pos.copy())
                                counter = 0
                                pos = []
                        else:
                            counter = 1
                            pos = [(i, j)]
                            stone = self.board.board[(i, j)]
            counter = 0
            pos = []
            stone = None

        return pattern_position

    # transposes board and use find_pattern_row
    # this design choice minimizes code duplication
    def find_pattern_col(self, n):
        board_t = Board(self.board.size)
        for row in range(self.board.size):
            for col in range(self.board.size):
                board_t.board[(col, row)] = self.board.board[(row, col)]

        pattern_position_t = Pattern(board_t).find_pattern_row(n)
        pattern_position = {'black':[], 'white':[]}

        while(pattern_position_t['black']):
            tmp_t = pattern_position_t['black'].pop()
            tmp = [(row, col) for col, row in tmp_t]
            pattern_position['black'].append(tmp)

        while(pattern_position_t['white']):
            tmp_t = pattern_position_t['white'].pop()
            tmp = [(row, col) for col, row in tmp_t]
            pattern_position['white'].append(tmp)

        return pattern_position

    # flips board and use find_pattern_diag1
    def find_pattern_diag2(self, n):
        board_t = Board(self.board.size)
        for row in range(self.board.size):
            for col in range(self.board.size):
                board_t.board[(self.board.size-1-row, col)] = self.board.board[(row, col)]

        pattern_position_t = Pattern(board_t).find_pattern_diag1(n)
        pattern_position = {'black':[], 'white':[]}

        while(pattern_position_t['black']):
            tmp_t = pattern_position_t['black'].pop()
            tmp = [(self.board.size-1-row, col) for row, col in tmp_t]
            pattern_position['black'].append(tmp)

        while(pattern_position_t['white']):
            tmp_t = pattern_position_t['white'].pop()
            tmp = [(self.board.size-1-row, col) for row, col in tmp_t]
            pattern_position['white'].append(tmp)

        return pattern_position

class Strategy():
    """Strategy class includes two strategy building blocks, i.e. strat_block
    and strat_extend. choose_move method uses these two building blocks to
    specify the computer's overall strategy in a clear and readable manner.
    """
    def __init__(self):
        pass

    def choose_move(self, board, stone):

        move = self.strat_extend(board, stone, 4)
        if move is not None:
            return move

        move = self.strat_block(board, stone, 4)
        if move is not None:
            return move

        move = self.strat_block(board, stone, 3)
        if move is not None:
            return move

        move = self.strat_extend(board, stone, 3)
        if move is not None:
            return move

        move = self.strat_extend(board, stone, 2)
        if move is not None:
            return move

        # if the strategies above suggest no moves, then choose at random
        # in the middle of the board. This is used mostly in the begainning
        # of the game.
        mid = round(board.size/2)
        row, col = mid, mid
        n = 0
        while not board.eval_move(row, col) and n<20:
            row = random.randint(mid-2, mid+2)
            col = random.randint(mid-2, mid+2)
            n += 1
        if n < 20:
            return (row, col)

        # this is used towards later in the game, when computer choose randomly
        # on the entire board. If after 100 times and yet a valid move has not
        # been found, computer will choose to fold by sending the code (999,999)
        n = 0
        while not board.eval_move(row, col) and n<100:
            row = random.randint(0, board.size-1)
            col = random.randint(0, board.size-1)
            n += 1
        if n<100:
            return (row, col)
        else:
            return (999, 999)

    def strat_block(self, board, stone, n):
        """When opponent has made n in a row, block opponent. This section has
        some code repetition and there might be an elegant way to extract the
        logic into a separate method. However, as is, readability is good."""

        if stone.color == 'black':
            opponent_color = 'white'
        else:
            opponent_color = 'black'

        pattern = Pattern(board)

        pattern_pos = pattern.find_pattern_row(n)
        while(pattern_pos[opponent_color]):
            pos = pattern_pos[opponent_color].pop()

            row = pos[0][0]
            col = pos[0][1]-1
            valid = board.eval_move(row, col)
            if valid:
                return (row, col)

            row = pos[len(pos)-1][0]
            col = pos[len(pos)-1][1]+1
            valid = board.eval_move(row, col)
            if valid:
                return (row, col)

        pattern_pos = pattern.find_pattern_col(n)
        while(pattern_pos[opponent_color]):
            pos = pattern_pos[opponent_color].pop()

            row = pos[0][0]-1
            col = pos[0][1]
            valid = board.eval_move(row, col)
            if valid:
                return (row, col)

            row = pos[len(pos)-1][0]+1
            col = pos[len(pos)-1][1]
            valid = board.eval_move(row, col)
            if valid:
                return (row, col)

        pattern_pos = pattern.find_pattern_diag1(n)
        while(pattern_pos[opponent_color]):
            pos = pattern_pos[opponent_color].pop()

            row = pos[0][0]+1
            col = pos[0][1]-1
            valid = board.eval_move(row, col)
            if valid:
                return (row, col)

            row = pos[len(pos)-1][0]-1
            col = pos[len(pos)-1][1]+1
            valid = board.eval_move(row, col)
            if valid:
                return (row, col)

        pattern_pos = pattern.find_pattern_diag2(n)
        while(pattern_pos[opponent_color]):
            pos = pattern_pos[opponent_color].pop()

            row = pos[0][0]-1
            col = pos[0][1]-1
            valid = board.eval_move(row, col)
            if valid:
                return (row, col)

            row = pos[len(pos)-1][0]+1
            col = pos[len(pos)-1][1]+1
            valid = board.eval_move(row, col)
            if valid:
                return (row, col)

        return None

    def strat_extend(self, board, stone, n):
        """When player has made n in a row, extend. The moves to extend are the
        same as the moves taken when opponent tries to block."""

        if stone.color == 'black':
            opponent_stone = Stone('white')
        else:
            opponent_stone = Stone('black')

        return self.strat_block(board, opponent_stone, n)

class Player:
    """Player class is a parent class that stores the name and stone.
    """

    def __init__(self, name, color):
        self.name = name
        self.stone = Stone(color)

    def play(self):
        print("{}'s turn".format(self.name))

class Player_Human(Player):
    """Player_Human class has procedures to ask human player for input.
    """

    def __init__(self, name, stone):
        super().__init__(name, stone)

    def play(self, board):

        super().play()
        valid = False

        while(not valid):

            while True:
                try:
                    row = int(input("row: "))
                    col = int(input("col: "))
                except ValueError:
                    print("Not an integer. Please try again.")
                    continue
                else:
                    break

            valid = board.eval_move(row-1, col-1)
            if not valid:
                print("""
                Invalid move. Please make sure that values provided
                are within the board size, and position does not overlap with
                existing stones.""")

        board.board[row-1, col-1] = self.stone

class Player_Computer(Player):
    """Player_Computer has procedures to let computer to play the next move.
    """
    def __init__(self, name, stone):
        super().__init__(name, stone)
        self.strategy = Strategy()

    def play(self, board):

        super().play()
        time.sleep(1)
        row, col = self.strategy.choose_move(board, self.stone)

        if row == 999 and col == 999:  # fold
            return 999

        if board.eval_move(row, col):
            board.board[row, col] = self.stone
        else:
            print("""
            Invalid move attempted by Computer {}. Please fix the
            computer algorithm. Position attempted: ({}, {})""".format(
            self.name, row+1, col+1))

            sys.exit()

class Gomoku:
    """Gomoku class manages data and overall flow of the game.
    """

    def __init__(self,
                 board,
                 player1,
                 player2):

        self.board = board
        self.player1 = player1
        self.player2 = player2

        self.steps = 0
        self.finished = False
        self.turn = self.player1
        self.winner = None

        system('clear')
        print('Step:', self.steps, '\n')
        print(board)

    def game(self):

        x1, x2 = None, None  # x1 and x2 are indicators if player folds

        while not self.finished:
            self.steps += 1

            if self.turn == self.player1:
                x1 = self.player1.play(self.board)
                self.turn = self.player2
            else:
                x2 = self.player2.play(self.board)
                self.turn = self.player1

            pattern_pos = self.board.eval_win()
            if pattern_pos is not None:
                self.finished = True
                self.board.pattern_pos = pattern_pos
            if x1 == 999 or x2 == 999:
                self.finished = True

            system('clear')
            print('Step:', self.steps, '\n')
            print(self.board)

        if self.steps == self.board.size ** 2 + 1 and pattern_pos is None:
            print('Draw! What a game!')
        if x1 == 999:
            print('{} folds.'.format(self.player1.name))
        elif x2 == 999:
            print('{} folds.'.format(self.player2.name))
        else:
            if self.turn == self.player1:
                self.winner = self.player2
            else:
                self.winner = self.player1
            print('{} has won!'.format(self.winner.name))

if __name__ == "__main__":

    try:
        _, p1_type, p1_name, p2_type, p2_name, size = sys.argv
        if p1_type not in ['human', 'computer']:
            raise ValueError
        if p2_type not in ['human', 'computer']:
            raise ValueError
        if size not in ['9', '13', '19']:
            raise ValueError

    except ValueError:
        print("""
        Please use the following format.
        python Play_Gomoku.py p1_type p1_name p2_type p2_name board_size.

        p1_type, p2_type be either human or computer.
        p1_name, p2_name can each be a string without space.
        board_size are integer values 9, 13 and 19.
        """)

        sys.exit()

    board = Board(int(size))
    if p1_type == 'human':
        p1 = Player_Human(p1_name, 'black')
    else:
        p1 = Player_Computer(p1_name, 'black')

    if p2_type == 'human':
        p2 = Player_Human(p2_name, 'white')
    else:
        p2 = Player_Computer(p2_name, 'white')

    gomoku = Gomoku(board, p1, p2)
    gomoku.game()
