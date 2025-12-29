from core.render.trees.binary_tree_graphviz import binary_tree_to_dot
from core.structures.trees.binary_tree import BinaryTree


def test_binary_tree_graphviz_smoke() -> None:
    bt: BinaryTree[int] = BinaryTree()
    bt.insert(1)
    bt.insert(2)
    dot = binary_tree_to_dot(bt.root)
    assert isinstance(dot, str)
    assert "digraph" in dot or "graph" in dot
