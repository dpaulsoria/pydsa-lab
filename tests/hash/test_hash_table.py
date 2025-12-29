import pytest

from core.structures.hash.hash_table import HashTable


def test_set_get_update_delete() -> None:
    ht = HashTable[str, int](capacity=4)
    ht.set("a", 1)
    ht.set("b", 2)
    assert ht.get("a") == 1
    ht.set("a", 99)
    assert ht.get("a") == 99
    assert ht.delete("b") is True
    assert ht.delete("b") is False
    with pytest.raises(KeyError):
        ht.get("b")


def test_resize_keeps_items() -> None:
    ht = HashTable[str, int](capacity=2)
    for i in range(20):
        ht.set(f"k{i}", i)
    for i in range(20):
        assert ht.get(f"k{i}") == i
