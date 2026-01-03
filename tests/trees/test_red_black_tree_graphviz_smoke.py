from core.render.trees.red_black_tree_graphviz import red_black_tree_to_dot
from core.structures.trees.red_black_tree import RedBlackTree


def test_rbt_to_dot_empty_smoke() -> None:
    dot = red_black_tree_to_dot(None)
    assert "digraph" in dot


def test_rbt_to_dot_non_empty_smoke() -> None:
    t = RedBlackTree[int]()
    for v in [2, 1, 3]:
        t.insert(v)
    dot = red_black_tree_to_dot(t.root, highlight=[1, 2])
    assert "digraph" in dot
