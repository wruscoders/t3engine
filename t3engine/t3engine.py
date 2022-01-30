import copy
from enum import Enum
import json
import functools

from t3engine import pub_mixin, pub


class state():
    """The state class holds the current state of a TicTacToe game.
    """

    class dir(Enum):
        """ An enumeration used to describe how the game ended.

        When the game has ended, this enumeration helps describe
        the condition that ended the game. ROW, COL, DIAG, and
        ANTI_DIAG are used when a player has won to indicate the
        direction of their victory. When combined with the
        coordinates of the last move, it identifies where the
        three in a row condition was met. The DRAW value is used
        when the last move caused a draw.
        """
        ROW = 0
        COL = 1
        DIAG = 2
        ANTI_DIAG = 3
        DRAW = 4

    def __init__(self):
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.turn = 0
        self.game_over = False
        self.winner = None
        self.winning_move = None
        self.winning_direction = None
        self.num_turns = 0

    def _create_board(self, s):
        """ Testing utility function used to initialize a board.

        The _create_board function takes a string representing the
        desired board state and sets up the board to match that state.
        For example,

        g.state._create_board("xox"
                        "xo "
                        " o "
                        )

        Args:
            s: a string representation of the desired board state
        """
        token = {
            '0': 0,
            'o': 0,
            'O': 0,
            '1': 1,
            'x': 1,
            'X': 1,
            ' ': None
        }
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        for i, ch in enumerate(s):
            t = token[ch]
            self.board[i % 3][i//3] = t
            if t != None:
                self.num_turns += 1

    def _print_board(self):
        """ A utility function for debugging that prints the board state.

        This function renders the current board state to stdout. It is
        a debugging tool.
        """
        ui = {0: 'X', 1: 'O', None: ' '}
        print('---')
        for i in range(0, 9):
            print(f'{ui[self.board[i%3][i//3]]}', end='')
            if i % 3 == 2:
                print()
        print('---')
        print()


class game(pub_mixin):

    def __init__(self):
        super().__init__()
        self.players = []
        self.state = state()

    @pub
    def join(self, p):
        self.players.append(p)
        p.game = self

    @pub
    def leave(self, p):
        p.game = None
        self.players.remove(p)

    @pub
    def move(self, x, y):
        if self.state.game_over:
            raise RuntimeError
        if self.state.board[x][y]:
            raise ValueError

        self.state.num_turns += 1
        self.state.board[x][y] = self.state.turn

        if self._check_end_game(x, y):
            return

        self.state.turn = (self.state.turn + 1) % 2

    def play(self):
        while not self.state.game_over:
            self.players[self.state.turn].play(self.state)

    def _declare_victory(self, player, x, y, dir):
        self.state.game_over = True
        self.state.winner = player
        self.state.winning_move = (x, y)
        self.state.winning_direction = dir

    def _check_end_game(self, x, y):
        turn = self.state.turn

        # Check row
        row = [self.state.board[x][y] for x in range(0, 3)]
        if row.count(turn) == 3:
            self._declare_victory(turn, x, y, state.dir.ROW)
            return True

        # Check col
        col = [self.state.board[x][y] for y in range(0, 3)]
        if col.count(turn) == 3:
            self._declare_victory(turn, x, y, state.dir.COL)
            return True

        # Check diagonals
        if x == y:
            diag = [self.state.board[i][i] for i in range(0, 3)]
            if diag.count(turn) == 3:
                self._declare_victory(turn, x, y, state.dir.DIAG)
                return True
        if x == 2-y:
            anti_diag = [self.state.board[i][2-i] for i in range(0, 3)]
            if anti_diag.count(turn) == 3:
                self._declare_victory(turn, x, y, state.dir.ANTI_DIAG)
                return True

        if self.state.num_turns == 9:
            self._declare_victory(None, None, None, state.dir.DRAW)
            return True

        return False
