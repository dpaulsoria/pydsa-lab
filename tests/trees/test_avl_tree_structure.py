from core.structures.trees.avl_tree import AVLTree


def test_avl_rotates_ll() -> None:
    t = AVLTree[int]()
    assert t.insert(3)
    assert t.insert(2)
    assert t.insert(1)  # fuerza rotación
    assert t.inorder() == [1, 2, 3]
    assert t.is_valid_avl()


def test_avl_delete_and_balance() -> None:
    t = AVLTree[int]()
    for v in [10, 20, 30, 40, 50, 25]:
        assert t.insert(v)
    assert t.is_valid_avl()

    assert t.delete(40)
    assert t.is_valid_avl()
    assert t.contains(25)
    assert not t.contains(999)
