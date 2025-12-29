from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Generic, TypeVar

T = TypeVar("T")


class OpKind(StrEnum):
    ENQUEUE = "enqueue"
    DEQUEUE = "dequeue"
    FRONT = "front"
    TO_LIST = "to_list"
    IS_EMPTY = "is_empty"
    CLEAR = "clear"


@dataclass
class Queue(Generic[T]):
    _items: deque[T] = field(default_factory=deque)

    def enqueue(self, item: T) -> None:
        self._items.append(item)

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def front(self) -> T | None:
        return self._items[0] if self._items else None

    def to_list(self) -> list[T]:
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return bool(self._items)

    def is_empty(self) -> bool:
        return not self._items

    def clear(self) -> None:
        self._items.clear()
