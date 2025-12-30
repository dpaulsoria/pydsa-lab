from __future__ import annotations

from core.render.trees.binary_search_tree_graphviz import binary_search_tree_to_dot
from core.structures.trees.binary_search_tree import BinarySearchTree


def test_bst_graphviz_to_dot_smoke() -> None:
    t: BinarySearchTree[int] = BinarySearchTree()
    for v in [4, 2, 6, 1, 3, 5, 7]:
        t.insert(v)

    dot = binary_search_tree_to_dot(t.root, highlight_values=[4, 2], highlight_target=5)
    assert isinstance(dot, str)
    assert "digraph" in dot
