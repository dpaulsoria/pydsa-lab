from core.algos.trees.avl_tree_ops import build_steps, parse_operations
from core.render.trees.avl_tree_graphviz import avl_tree_to_dot


def test_avl_ops_basic() -> None:
    ops = parse_operations("insert 3\ninsert 2\ninsert 1\nbfs\n")
    steps = build_steps(ops, dot_builder=avl_tree_to_dot)
    assert steps[-1].bfs == [2, 1, 3]
