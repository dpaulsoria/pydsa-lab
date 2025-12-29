from core.structures.linear.skip_list import SkipList


def test_skip_list_insert_search_delete() -> None:
    sl = SkipList[int](max_level=6, seed=7)

    assert sl.insert(10, level=2) is True
    assert sl.insert(20, level=0) is True
    assert sl.insert(30, level=1) is True
    assert len(sl) == 3

    assert sl.search(20) is True
    assert sl.search(99) is False

    assert sl.delete(10) is True
    assert sl.delete(10) is False
    assert sl.search(10) is False
    assert len(sl) == 2
