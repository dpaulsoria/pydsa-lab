from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    value: T
    next: Node[T] | None = None


class LinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Node[T] | None = None
        self._size: int = 0

    def push_front(self, value: T) -> None:
        self.head = Node(value, self.head)
        self._size += 1

    def append(self, value: T) -> None:
        if self.head is None:
            self.head = Node(value)
            self._size += 1
            return  # Prevent duplicates

        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = Node(value)
        self._size += 1

    def delete(self, value: T) -> bool:
        if self.head is None:
            return False

        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1
            return True

        prev = self.head
        cur = self.head.next

        while cur is not None:
            if cur.value == value:
                prev.next = cur.next
                self._size -= 1
                return True
            prev = cur
            cur = cur.next

        return False

    def delete_all(self, value: T) -> int:
        count = 0

        while self.head is not None and self.head.value == value:
            self.head = self.head.next
            count += 1

        prev = self.head
        cur = self.head.next if self.head is not None else None

        while cur is not None:
            if cur.value == value:
                prev.next = cur.next
                count += 1
                cur = prev.next
            else:
                prev = cur
                cur = cur.next

        self._size -= count
        return count

    def delete_at(self, index: int) -> T:
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        if self.head is None:
            raise IndexError("delete_at from empty list")

        if index == 0:
            removed = self.head
            self.head = self.head.next
            self._size -= 1
            return removed.value

        prev = self.head
        cur_index = 0
        while cur_index < index - 1:
            prev = prev.next
            cur_index += 1

        removed = prev.next
        prev.next = removed.next
        self._size -= 1

        return removed.value

    def find_index(self, value: T) -> int | None:
        idx = 0
        cur = self.head
        while cur is not None:
            if cur.value == value:
                return idx
            idx += 1
            cur = cur.next
        return None

    def to_list(self) -> list[T]:
        out: list[T] = []
        cur = self.head
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out

    def __len__(self) -> int:
        return self._size
