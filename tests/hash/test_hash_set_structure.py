from __future__ import annotations

from typing import Any

from core.structures.hash.hash_set import HashSet


def test_hash_set_basic_add_remove_contains_snapshot() -> None:
    s: HashSet[Any] = HashSet(capacity=4)

    assert len(s) == 0
    assert s.contains(1) is False

    s.add(1)
    s.add(2)
    s.add(1)  # si es set real, no duplica

    assert s.contains(1) is True
    assert s.contains(2) is True

    values = s.to_list()
    assert isinstance(values, list)
    # Debe ser "set-like": sin duplicados
    assert len(values) == len(set(values))

    assert s.remove(1) is True
    assert s.contains(1) is False
    assert s.remove(1) is False  # ya no está

    snap = s.snapshot()
    assert isinstance(snap, dict)
    assert "buckets" in snap
    assert "capacity" in snap
    assert isinstance(snap["buckets"], list)
    assert int(snap["capacity"]) > 0
