from typing import List, Union


class Position:

    def __init__(self, x, y):

        self.x = x
        self.y = y

    def __eq__(self, other):
        return (
                isinstance(other, Position)
                and other.x == self.x
                and other.y == self.y
        )

    def __hash__(self):
        return self.x*10 + self.y


class GameState:

    def __init__(self, to_play=1):
        """
        Player 1 has the first move
        """
        self.to_play = to_play
        self.board = None

    def do_move(self, move: Position):
        """

        """
        new_state = GameState(to_play=3 - self.to_play)

        return new_state

    def get_moves(self):
        """
        Get all possible moves from this state.
        """

    def get_result(self, player: int):
        """
        Get the game result from the viewpoint of player.
        """

    def __repr__(self):
        pass


class XOXState(GameState):

    def __init__(self, to_play=1, board=None):
        super().__init__(to_play=to_play)
        self.dim_size = 3
        if board:
            self.board =board
        else:
            self.board = [[0] * self.dim_size for i in [0] * self.dim_size]

    def _is_free(self, move: Position) -> bool:

        return self.board[move.x][move.y] == 0

    def do_move(self, move: Position) -> GameState:

        assert move.x in range(self.dim_size)
        assert move.y in range(self.dim_size)
        assert self._is_free(move)

        new_state = XOXState(to_play=-self.to_play)
        new_state.board = [x[:] for x in self.board]
        new_state.board[move.x][move.y] = self.to_play

        return new_state

    def get_moves(self) -> List[Position]:

        result = self.get_result(player=1)

        if result in [1.0, 0.0, 0.5]:
            return []

        return [
            Position(x, y)
            for x, line in enumerate(self.board)
            for y, cell in enumerate(line) if cell == 0
        ]

    def get_result(self, player: int) -> Union[float, None]:

        """
        012
        345
        678
        """

        row_sum = [sum(x) for x in self.board]
        column_sum = [sum(x) for x in zip(*self.board)]
        r_diag_sum = sum([self.board[x][x] for x in range(self.dim_size)])
        l_diag_sum = sum(
            [self.board[x][self.dim_size-1-x] for x in range(self.dim_size)]
        )

        player_win = any([x == player * self.dim_size for x in row_sum])
        player_win += any([x == player * self.dim_size for x in column_sum])
        player_win += (r_diag_sum == player * self.dim_size)
        player_win += (l_diag_sum == player * self.dim_size)

        other_win = any([x == -player * self.dim_size for x in row_sum])
        other_win += any([x == -player * self.dim_size for x in column_sum])
        other_win += (r_diag_sum == -player * self.dim_size)
        other_win += (l_diag_sum == -player * self.dim_size)

        if player_win:
            return 1.0

        elif other_win:
            return 0.0

        elif all(x != 0 for x in sum(self.board, [])):
            return 0.5

        else:
            return None

    def game_over(self) -> bool:

        if self.get_result(player=1):
            return True

        return False

    def __repr__(self):

        s = "\n"

        for i in range(3):
            for j in range(3):
                s += ".XO"[self.board[i][j]]
                if j == 2:
                    s += "\n"
        return s


class Domineering(GameState):
    """
    todo
    """

    def __init__(self, to_play=1, board_size=3):
        super().__init__(to_play=to_play)
        self.board_size = board_size
        self.board = ['.'*self.board_size]*self.board_size

    def do_move(self, move):
        pass

    def __repr__(self):

        s = "\n"

        for line in range(self.board_size):
            s += "%s\n" % "".join(self.board[line])

        return s
