from unittest import TestCase

from py_mcts.uct import UCTNode
from py_mcts.state import XOXState, Position


class UCTTest(TestCase):

    def setUp(self):

        self.xox_state = XOXState()
        self.node = UCTNode(game_state=self.xox_state)

    def test_add_children(self):

        self.node.add_child(move=Position(0, 1))

        # non empty children dict
        self.assertTrue(self.node.children)
        assert list(self.node.children.keys()) == [Position(0, 1)]

        # child parent
        child = self.node.children[Position(0, 1)]
        assert child.parent == self.node

    def test_select_leaf(self):

        self.node.expand()
        leaf = self.node.select_leaf()

        self.assertIn(leaf, self.node.children.values())

    def test_play_out(self):

        self.node.expand()
        leaf = self.node.select_leaf()

        result_state = leaf.play_out()

        # no more moves
        self.assertFalse(result_state.get_moves())

        # result state result
        self.assertIn(result_state.get_result(player=1), [1.0, 0.0, 0.5])

    def test_backup(self):
        # self.node.expand()
        leaf = self.node.select_leaf()

        result_state = leaf.play_out()

        leaf.backup(result_state)
        self.assertIn(leaf.Q(), [value for value in [0.0, 1.0, 0.5]])
