import random
from math import sqrt, log


class UCTNode:

    def __init__(self, game_state, parent=None):

        self.game_state = game_state
        self.parent = parent
        self.children = {}
        self.is_expanded = False

        self.total_value = 0
        self.number_visits = 0

    def add_child(self, move):
        """
        add child to children variable
        {move: child_state}
        """
        self.children[move] = UCTNode(
            game_state=self.game_state.do_move(move),
            parent=self,
        )

    def expand(self):
        """
        Add all possible children to current node
        """
        self.is_expanded = True

        possible_moves = self.game_state.get_moves()

        for move in possible_moves:
            self.add_child(move=move)

    def Q(self):
        """

        """
        if self.number_visits == 0:
            return float("inf")

        return self.total_value / self.number_visits

    def U(self):
        """

        """
        if self.number_visits == 0:
            return float("inf")

        return 2 * sqrt(
            log(self.parent.number_visits)/self.number_visits
        )

    def best_child(self):
        """
        Select best child based on UCB1 formula
        """
        return max(
            self.children.values(),
            key=lambda node: node.Q() + node.U()
        )

    def select_leaf(self):
        leaf = self
        while leaf.is_expanded and leaf.children:
            leaf = leaf.best_child()

        return leaf

    def play_out(self):
        """
        Full game simulation and return result state
        """
        tmp_state = self.game_state

        while tmp_state.get_moves():
            possible_moves = tmp_state.get_moves()
            tmp_state = tmp_state.do_move(random.choice(possible_moves))

        return tmp_state

    def backup(self, simulation_final_state):
        """
        Based on simulation final state
        back propagate value to parent states
        """
        current = self

        while current:
            current.number_visits += 1
            current.total_value += simulation_final_state.get_result(
                -current.game_state.to_play
            )
            current = current.parent


class MCTS:

    def __init__(self, node: UCTNode):

        self.root = node
        self.root.expand()

    def _select(self):

        leaf = self.root.select_leaf()

        return leaf

    @staticmethod
    def _expand_and_simulate(leaf):

        if leaf.number_visits != 0:
            leaf.expand()
            leaf = leaf.select_leaf()
        play_out_state = leaf.play_out()

        return play_out_state

    def best_move(self, it: int):

        for _ in range(it):

            leaf = self._select()
            play_out_state = self._expand_and_simulate(leaf)
            leaf.backup(play_out_state)

        # Get best move
        result = max(
            self.root.children.items(),
            key=lambda item: item[1].number_visits
        )

        return result[0], result[1]
