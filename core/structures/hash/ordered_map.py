from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

from core.structures.hash.hash_table import HashTable

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class _Node(Generic[K, V]):
    key: K
    value: V
    prev: _Node[K, V] | None = None
    next: _Node[K, V] | None = None


class OrderedMap(Generic[K, V]):
    def __init__(self, capacity: int = 8) -> None:
        self._index: HashTable[K, _Node[K, V]] = HashTable(capacity=capacity)
        self._head: _Node[K, V] | None = None
        self._tail: _Node[K, V] | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def set(self, key: K, value: V) -> None:
        # update si existe
        try:
            node = self._index.get(key)
            node.value = value
            return
        except KeyError:
            pass

        node = _Node(key, value)

        if self._tail is None:
            self._head = self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node

        self._index.set(key, node)
        self._size += 1

    def get(self, key: K) -> V:
        node = self._index.get(key)
        return node.value

    def delete(self, key: K) -> bool:
        try:
            node = self._index.get(key)
        except KeyError:
            return False

        # unlink en lista
        if node.prev is None:
            self._head = node.next
        else:
            node.prev.next = node.next

        if node.next is None:
            self._tail = node.prev
        else:
            node.next.prev = node.prev

        node.prev = node.next = None

        self._index.delete(key)
        self._size -= 1
        return True

    def items(self) -> Iterable[tuple[K, V]]:
        cur = self._head
        while cur is not None:
            yield (cur.key, cur.value)
            cur = cur.next

    def snapshot(self) -> dict[str, object]:
        # orden de inserción
        ordered = list(self.items())
        # buckets del hash (para visualizar colisiones + refs)
        s = self._index.snapshot()
        buckets = [[(k, "•") for (k, _node) in b] for b in s["buckets"]]
        return {
            "capacity": s["capacity"],
            "size": self._size,
            "load_factor": s["load_factor"],
            "ordered": ordered,
            "buckets": buckets,
        }
