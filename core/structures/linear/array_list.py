from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class ArrayList(Generic[T]):
    _items: list[T]

    def __init__(self) -> None:
        self._items = []

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return bool(self._items)

    def is_empty(self) -> bool:
        return not self._items

    def to_list(self) -> list[T]:
        return list(self._items)

    def get(self, index: int) -> T:
        return self._items[index]

    def set(self, index: int, value: T) -> None:
        self._items[index] = value

    def append(self, value: T) -> None:
        self._items.append(value)

    def insert(self, index: int, value: T) -> None:
        self._items.insert(index, value)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty ArrayList")
        return self._items.pop()

    def pop_at(self, index: int) -> T:
        if not self._items:
            raise IndexError("pop_at from empty ArrayList")
        return self._items.pop(index)

    def remove_first(self, value: T) -> bool:
        try:
            self._items.remove(value)
            return True
        except ValueError:
            return False

    def clear(self) -> None:
        self._items.clear()
