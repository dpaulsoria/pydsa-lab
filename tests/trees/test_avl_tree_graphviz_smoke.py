from core.render.trees.avl_tree_graphviz import avl_tree_to_dot
from core.structures.trees.avl_tree import AVLTree


def test_avl_to_dot_empty_smoke() -> None:
    dot = avl_tree_to_dot(None)
    assert "digraph" in dot


def test_avl_to_dot_non_empty_smoke() -> None:
    t = AVLTree[int]()
    for v in [2, 1, 3]:
        t.insert(v)
    dot = avl_tree_to_dot(t.root, highlight=[1, 2])
    assert "digraph" in dot
