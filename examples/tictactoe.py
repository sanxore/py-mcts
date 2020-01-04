from py_mcts.state import XOXState, Position
from py_mcts.uct import MCTS, UCTNode


if __name__ == '__main__':

    xox = XOXState()
    print("init state:")
    print(xox)
    print("what is your name:")
    p1_name = input()
    while xox.get_moves():

        print("%s chose a position comma separated ex: 1,2:" % p1_name)
        p1_x, p1_y = input().split(",")

        xox = xox.do_move(Position(int(p1_x), int(p1_y)))
        print("%s move: " % p1_name)
        print(xox)

        if xox.game_over():
            break

        print("Jack is thinking ...")
        uct_node = UCTNode(game_state=xox)
        mcts = MCTS(node=uct_node)
        jack_move, best_node = mcts.best_move(it=10000)

        xox = xox.do_move(jack_move)
        print("Jack move: ")
        print(xox)

        print("U=%s" % best_node.U())
        print("Q=%s" % best_node.Q())
        if xox.game_over():
            break

    result = xox.get_result(player=-1)

    if result == 1.0:
        print("Jack Win.")
    elif result == 0.0:
        print("%s Win." % p1_name)
    else:
        print("No one Win.")

