from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


def stable_hash(key: object) -> int:
    """Hash determinístico (útil para visualización)."""
    if isinstance(key, int):
        return key & 0xFFFFFFFF
    if isinstance(key, str):
        h = 2166136261  # FNV-ish simple
        for ch in key:
            h ^= ord(ch)
            h = (h * 16777619) & 0xFFFFFFFF
        return h
    return hash(key) & 0xFFFFFFFF


@dataclass
class Entry(Generic[K, V]):
    key: K
    value: V


class HashTable(Generic[K, V]):
    def __init__(self, capacity: int = 8) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self._buckets: list[list[Entry[K, V]]] = [[] for _ in range(capacity)]
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def capacity(self) -> int:
        return len(self._buckets)

    def load_factor(self) -> float:
        return self._size / self.capacity()

    def _index(self, key: K) -> int:
        return stable_hash(key) % self.capacity()

    def _maybe_resize(self) -> None:
        if self.load_factor() <= 0.75:
            return
        self._rehash(self.capacity() * 2)

    def _rehash(self, new_capacity: int) -> None:
        old_items = list(self.items())
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0
        for k, v in old_items:
            self.set(k, v)

    def set(self, key: K, value: V) -> None:
        idx = self._index(key)
        bucket = self._buckets[idx]
        for e in bucket:
            if e.key == key:
                e.value = value
                return
        bucket.append(Entry(key, value))
        self._size += 1
        self._maybe_resize()

    def get(self, key: K) -> V:
        idx = self._index(key)
        bucket = self._buckets[idx]
        for e in bucket:
            if e.key == key:
                return e.value
        raise KeyError(key)

    def has(self, key: K) -> bool:
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def delete(self, key: K) -> bool:
        idx = self._index(key)
        bucket = self._buckets[idx]
        for i, e in enumerate(bucket):
            if e.key == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def items(self) -> Iterable[tuple[K, V]]:
        for bucket in self._buckets:
            for e in bucket:
                yield (e.key, e.value)

    def snapshot(self) -> dict[str, object]:
        return {
            "capacity": self.capacity(),
            "size": self._size,
            "load_factor": self.load_factor(),
            "buckets": [[(e.key, e.value) for e in b] for b in self._buckets],
        }
