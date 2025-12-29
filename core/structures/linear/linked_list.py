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
            return

        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = Node(value)
        self._size += 1

    def _node_at(self, index: int) -> Node[T]:
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")

        cur = self.head
        for _ in range(index):
            assert cur is not None
            cur = cur.next

        assert cur is not None
        return cur

    def _unlink_head(self) -> Node[T]:
        if self.head is None:
            raise IndexError("unlink_head from empty list")
        removed = self.head
        self.head = removed.next
        removed.next = None
        self._size -= 1
        return removed

    def _unlink_after(self, prev: Node[T]) -> Node[T]:
        if prev.next is None:
            raise IndexError("unlink_after with no text node")
        removed = prev.next
        prev.next = removed.next
        removed.next = None
        self._size -= 1
        return removed

    def search(self, value: T) -> Node[T] | None:
        cur = self.head
        while cur is not None:
            if cur.value == value:
                return cur
            cur = cur.next
        return None

    def reverse(self) -> None:
        prev: Node[T] | None = None
        cur = self.head
        while cur is not None:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def delete(self, value: T) -> bool:
        if self.head is None:
            return False

        if self.head.value == value:
            self._unlink_head()
            return True

        prev = self.head
        cur = self.head.next
        while cur is not None:
            if cur.value == value:
                self._unlink_after(prev)
                return True
            prev = cur
            cur = cur.next

        return False

    def delete_all(self, value: T) -> int:
        dummy = Node(value, self.head)  # value no importa aquí
        prev = dummy
        cur = self.head
        removed_count = 0

        while cur is not None:
            if cur.value == value:
                # unlink cur: prev.next = cur.next
                prev.next = cur.next
                cur.next = None
                self._size -= 1
                removed_count += 1
                cur = prev.next
            else:
                prev = cur
                cur = cur.next

        self.head = dummy.next
        return removed_count

    def delete_at(self, index: int) -> T:
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")

        if index == 0:
            return self._unlink_head().value

        prev = self._node_at(index - 1)
        return self._unlink_after(prev).value

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
