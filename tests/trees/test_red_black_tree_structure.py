from core.structures.trees.red_black_tree import RedBlackTree


def test_rbt_insert_inorder_sorted_and_valid() -> None:
    t = RedBlackTree[int]()
    for v in [10, 20, 30, 15, 25, 5, 1, 7]:
        assert t.insert(v)
        assert t.is_valid_llrb()

    assert t.inorder() == sorted([10, 20, 30, 15, 25, 5, 1, 7])
    assert not t.insert(10)  # no duplicates
    assert t.is_valid_llrb()


def test_rbt_delete_keeps_valid() -> None:
    t = RedBlackTree[int]()
    for v in [4, 2, 6, 1, 3, 5, 7]:
        t.insert(v)

    assert t.is_valid_llrb()
    assert t.delete(6)
    assert t.is_valid_llrb()
    assert not t.contains(6)

    assert t.delete(4)  # borra root
    assert t.is_valid_llrb()
    assert t.inorder() == [1, 2, 3, 5, 7]

    assert not t.delete(999)  # no existe
    assert t.is_valid_llrb()
