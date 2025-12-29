from __future__ import annotations

from typing import Generic, TypeVar

from core.structures.hash.hash_table import HashTable

T = TypeVar("T")

_PRESENT = object()


class HashSet(Generic[T]):
    def __init__(self, capacity: int = 8) -> None:
        self._ht: HashTable[T, object] = HashTable(capacity=capacity)

    def __len__(self) -> int:
        return len(self._ht)

    def add(self, value: T) -> None:
        self._ht.set(value, _PRESENT)

    def contains(self, value: T) -> bool:
        return self._ht.has(value)

    def remove(self, value: T) -> bool:
        return self._ht.delete(value)

    def to_list(self) -> list[T]:
        return [k for k, _ in self._ht.items()]

    def snapshot(self) -> dict[str, object]:
        s = self._ht.snapshot()
        buckets = [[k for (k, _v) in b] for b in s["buckets"]]
        return {
            "capacity": s["capacity"],
            "size": s["size"],
            "load_factor": s["load_factor"],
            "buckets": buckets,
        }
