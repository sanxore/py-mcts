from unittest import TestCase

from py_mcts.state import GameState, XOXState, Position


class GameStateTestCase(TestCase):

    def setUp(self):
        self.game_state = GameState()

    def test_move(self):

        # this move is made by the player 1
        new_state = self.game_state.do_move(2)

        # idempotent
        assert self.game_state.to_play == 1

        # so the player 2 is the next one to play
        assert new_state.to_play == 2


class XOXStateTestCase(TestCase):

    def setUp(self):
        self.xox_state = XOXState()

    def test_move(self):

        # player 1 fill cell 0,0
        new_state = self.xox_state.do_move(Position(0, 0))

        assert new_state.board == [[1, 0, 0], [0, 0, 0], [0, 0, 0]]

    def test_get_moves(self):

        # player 1 fill cell 0,0
        new_state = self.xox_state.do_move(Position(0, 0))

        possible_moves = new_state.get_moves()

        assert possible_moves == [
            Position(x, y)
            for x in range(3)
            for y in range(3)
            if x + y != 0
        ]

    def test_get_result_1(self):

        # player 1 win by felling the first line
        current_state = self.xox_state
        moves = [
            Position(0, 0),
            Position(1, 0),
            Position(0, 1),
            Position(1, 1),
            Position(0, 2),
        ]

        for p in moves:
            current_state = current_state.do_move(p)

        assert current_state.get_result(player=1) == 1.0
        assert current_state.get_result(player=-1) == 0.0

    def test_get_result_2(self):
        """
        012
        345
        678
        """

        # player -1 win by felling the second line
        current_state = self.xox_state
        moves = [
            Position(0, 0),
            Position(1, 0),
            Position(0, 1),
            Position(1, 1),
            Position(2, 2),
            Position(1, 2),
        ]

        for i in moves:
            current_state = current_state.do_move(i)

        assert current_state.get_result(player=1) == 0.0
        assert current_state.get_result(player=-1) == 1.0

    def test_get_result_before_end(self):

        current_state = self.xox_state
        moves = [
            Position(0, 0),
            Position(1, 0),
            Position(0, 1),
            Position(1, 1),
        ]

        for i in moves:
            current_state = current_state.do_move(i)

        self.assertIsNone(current_state.get_result(player=1))

    def test_get_result_no_one_win(self):

        current_state = self.xox_state
        moves = [
            Position(0, 0),
            Position(0, 1),
            Position(1, 1),
            Position(2, 2),
            Position(2, 0),
            Position(0, 2),
            Position(1, 2),
            Position(1, 0),
            Position(2, 1),
        ]
        for i in moves:
            current_state = current_state.do_move(i)

        assert current_state.get_result(player=-1) == 0.5


