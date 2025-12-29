from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class CDNode(Generic[T]):
    value: T
    prev: CDNode[T] | None = None
    next: CDNode[T] | None = None


class CircularDoublyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: CDNode[T] | None = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def is_empty(self) -> bool:
        return self._size == 0

    def push_front(self, value: T) -> None:
        node = CDNode(value)
        if self.head is None:
            node.next = node
            node.prev = node
            self.head = node
        else:
            head = self.head
            tail = head.prev
            assert tail is not None
            node.next = head
            node.prev = tail
            tail.next = node
            head.prev = node
            self.head = node

        self._size += 1

    def push_back(self, value: T) -> None:
        node = CDNode(value)
        if self.head is None:
            node.next = node
            node.prev = node
            self.head = node
        else:
            head = self.head
            tail = head.prev
            assert tail is not None

            node.prev = tail
            node.next = head
            tail.next = node
            head.prev = node

        self._size += 1

    def pop_front(self) -> T:
        if self.head is None:
            raise IndexError("pop_front from empty list")

        removed = self.head
        if self._size == 1:
            self.head = None
        else:
            head = self.head
            tail = head.prev
            new_head = head.next
            assert tail is not None and new_head is not None
            tail.next = new_head
            new_head.prev = tail
            self.head = new_head

        removed.next = None
        removed.prev = None
        self._size -= 1
        return removed.value

    def pop_back(self) -> T:
        if self.head is None:
            raise IndexError("pop_back from empty list")

        head = self.head
        tail = head.prev
        assert tail is not None
        removed = tail

        if self._size == 1:
            self.head = None
        else:
            new_tail = removed.prev
            assert new_tail is not None
            new_tail.next = head
            head.prev = new_tail

        removed.next = None
        removed.prev = None
        self._size -= 1
        return removed.value

    def rotate_left(self, k: int = 1) -> None:
        if self.head is None or self._size <= 1:
            return
        steps = k % self._size
        for _ in range(steps):
            assert self.head is not None and self.head.next is not None
            self.head = self.head.next

    def rotate_right(self, k: int = 1) -> None:
        if self.head is None or self._size <= 1:
            return
        steps = k % self._size
        for _ in range(steps):
            assert self.head is not None and self.head.prev is not None
            self.head = self.head.prev

    def find_index(self, value: T) -> int | None:
        if self.head is None:
            return None

        cur = self.head
        for i in range(self._size):
            if cur.value == value:
                return i
            assert cur.next is not None
            cur = cur.next
        return None

    def delete(self, value: T) -> bool:
        node = self._find_node(value)
        if node is None:
            return False
        self._unlink(node)
        return True

    def delete_all(self, value: T) -> int:
        if self.head is None:
            return 0
        removed = 0
        n = self._size
        cur = self.head
        for _ in range(n):
            if cur is None:
                break
            nxt = cur.next
            if cur.value == value:
                self._unlink(cur)
                removed += 1
                if self.head is None:
                    break
            cur = nxt
        return removed

    def to_list(self) -> list[T]:
        out: list[T] = []
        if self.head is None:
            return out
        cur = self.head
        for _ in range(self._size):
            out.append(cur.value)
            assert cur.next is not None
            cur = cur.next
        return out

    def to_reverse_list(self) -> list[T]:
        out: list[T] = []
        if self.head is None:
            return out
        cur = self.head
        for _ in range(self._size):
            out.append(cur.value)
            assert cur.prev is not None
            cur = cur.prev
        return out

    def _find_node(self, value: T) -> CDNode[T] | None:
        if self.head is None:
            return None
        cur = self.head
        for _ in range(self._size):
            if cur.value == value:
                return cur
            assert cur.next is not None
            cur = cur.next
        return None

    def _unlink(self, node: CDNode[T]) -> None:
        if self.head is None:
            return

        if self._size == 1:
            self.head = None
            node.next = None
            node.prev = None
            self._size = 0
            return

        prev_node = node.prev
        next_node = node.next
        assert prev_node is not None and next_node is not None

        prev_node.next = next_node
        next_node.prev = prev_node

        if node is self.head:
            self.head = next_node

        node.next = None
        node.prev = None
        self._size -= 1
