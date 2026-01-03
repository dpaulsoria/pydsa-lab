from core.algos.trees.red_black_tree_ops import build_steps, parse_operations
from core.render.trees.red_black_tree_graphviz import red_black_tree_to_dot


def test_rbt_ops_basic() -> None:
    ops = parse_operations("insert 3\ninsert 2\ninsert 1\nbfs\n")
    steps = build_steps(ops, dot_builder=red_black_tree_to_dot)
    assert steps[-1].inorder == [1, 2, 3]
