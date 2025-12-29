from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class DequeDS(Generic[T]):
    _items: deque[T] = field(default_factory=deque)

    def push_front(self, item: T) -> None:
        self._items.appendleft(item)

    def push_back(self, item: T) -> None:
        self._items.append(item)

    def pop_front(self) -> T:
        if not self._items:
            raise IndexError("pop_front from empty deque")
        return self._items.popleft()

    def pop_back(self) -> T:
        if not self._items:
            raise IndexError("pop_back from empty deque")
        return self._items.pop()

    def peek_front(self) -> T | None:
        return self._items[0] if self._items else None

    def peek_back(self) -> T | None:
        return self._items[-1] if self._items else None

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
