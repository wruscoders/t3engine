import pytest
from random import randint

from t3engine import game, state


class player_test():
    def __init__(self, name):
        self.game = None
        self.name = None


@pytest.fixture
def g():
    g = game()
    g.join(player_test('albert'))
    g.join(player_test('barbara'))
    return g


def test_game_init(g):
    assert g
    assert len(g.players) == 2
    assert g.players[0].game == g
    assert g.players[1].game == g
    assert not len(g.subs)
    assert g.state

def test__create_board(g):
    g.state._create_board("xxx"
                          "oo "
                          "   "
                          )

    assert g.state.board == [[1, 0, None], [1, 0, None], [1, None, None]]


def test_row_victory_x(g):
    g.state.turn = 1

    g.state._create_board("xxx"
                          "oo "
                          "   "
                          )
    assert g._check_victory(2, 0) == True
    assert g.state.winner == 1
    assert g.state.winning_direction == state.dir.ROW
    assert g.state.winning_move == (2, 0)


def test_row_victory_x2(g):
    g.state.turn = 1
    g.state._create_board("   "
                          "oo "
                          "xxx"
                          )

    assert g._check_victory(1, 2) == True
    assert g.state.winner == 1
    assert g.state.winning_direction == state.dir.ROW
    assert g.state.winning_move == (1, 2)


def test_row_continue(g):
    g.state.turn = 1
    g.state._create_board("   "
                          "o  "
                          "xx "
                          )
    assert g._check_victory(1, 2) == False
    assert g.state.winner == None
    assert g.state.winning_direction == None
    assert g.state.winning_move == None


def test_check_cols(g):
    g.state.turn = 0

    g.state._create_board("xox"
                          "xo "
                          " o "
                          )
    assert g._check_victory(1, 1) == True
    assert g.state.winner == 0
    assert g.state.winning_direction == state.dir.COL
    assert g.state.winning_move == (1, 1)


def test_check_diag(g):
    g.state.turn = 1
    g.state._create_board("xo "
                          "xxo"
                          " ox"
                          )
    assert g._check_victory(1, 1) == True
    assert g.state.winner == 1
    assert g.state.winning_direction == state.dir.DIAG
    assert g.state.winning_move == (1, 1)

def test_move(g):
    g.state.turn = 1
    g.move(1,1)
    
    assert g.state.board[1][1] == 1

def test_check_anti_diag(g):
    g.state.turn = 1
    g.state._create_board(" ox"
                          "xxo"
                          "xo "
                          )
    assert g._check_victory(1, 1) == True
    assert g.state.winner == 1
    assert g.state.winning_direction == state.dir.ANTI_DIAG
    assert g.state.winning_move == (1, 1)


class player_random():
    def __init__(self,name):
        self.game = None
        self.name = name

    def play(self):
        while True:
            x = randint(0, 2)
            y = randint(0, 2)
            if self.game.state.board[x][y] is None:
                self.game.move(x, y)
                return

def test_check_random_play():
    g = game()
    g.join(player_random('albert'))
    g.join(player_random('barbara'))
    g.play()

class sub():
    def __init__(self,g):
        g.sub(self)
    
    def pub(self,j):
        print(j)

def test_pub_state(g):
    s = sub(g)

    g.players[0].game.move(1,1)

