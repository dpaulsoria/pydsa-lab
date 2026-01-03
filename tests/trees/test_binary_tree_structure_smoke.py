from core.structures.trees.binary_tree import BinaryTree


def test_binary_tree_structure_smoke() -> None:
    bt: BinaryTree[int] = BinaryTree()
    assert bt.is_empty()

    bt.insert(10)
    bt.insert(20)
    bt.insert(30)

    assert len(bt) == 3
    assert bt.has(20) is True
    assert bt.has(99) is False

    assert bt.delete(20) is True
    assert bt.delete(99) is False
    assert len(bt) == 2

    bt.clear()
    assert len(bt) == 0
