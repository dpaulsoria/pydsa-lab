from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class DNode(Generic[T]):
    value: T
    prev: DNode[T] | None = None
    next: DNode[T] | None = None


class DoublyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: DNode[T] | None = None
        self.tail: DNode[T] | None = None
        self._size: int = 0

    def push_front(self, value: T) -> None:
        node = DNode(value, None, next=self.head)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.head.prev = node
            self.head = node
        self._size += 1

    def push_back(self, value: T) -> None:
        node = DNode(value, self.tail, None)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def pop_front(self) -> T:
        if self.head is None:
            raise IndexError("pop_front from empty list")

        removed = self.head
        new_head = removed.next

        if new_head is None:
            self.head = self.tail = None
        else:
            new_head.prev = None
            self.head = new_head

        self._size -= 1
        return removed.value

    def pop_back(self) -> T:
        if self.tail is None:
            raise IndexError("pop_back from empty list")

        removed = self.tail
        new_tail = removed.prev

        if new_tail is None:
            self.head = self.tail = None
        else:
            new_tail.next = None
            self.tail = new_tail

        self._size -= 1
        return removed.value

    def delete(self, value: T) -> bool:
        cur = self.head
        while cur is not None:
            if cur.value == value:
                self._unlink(cur)
                self._size -= 1
                return True
            cur = cur.next
        return False

    def delete_all(self, value: T) -> int:
        count = 0
        cur = self.head
        while cur is not None:
            nxt = cur.next
            if cur.value == value:
                self._unlink(cur)
                count += 1
            cur = nxt
        self._size -= count
        return count

    def delete_at(self, index: int) -> T:
        node = self._node_at(index)
        self._unlink(node)
        self._size -= 1
        return node.value

    def find_index(self, value: T) -> int | None:
        idx = 0
        cur = self.head
        while cur is not None:
            if cur.value == value:
                return idx
            cur = cur.next
            idx += 1
        return None

    def _node_at(self, index: int) -> DNode[T] | None:
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")

        if index <= self._size // 2:
            cur = self.head
            i = 0
            while i < index:
                cur = cur.next
                i += 1
            return cur
        else:
            cur = self.tail
            i = self._size - 1
            while i > index:
                cur = cur.prev
                i -= 1
            return cur

    def _unlink(self, node: DNode[T]) -> None:
        prev = node.prev
        nxt = node.next

        if prev is None:
            self.head = nxt
        else:
            prev.next = nxt

        if nxt is None:
            self.tail = prev
        else:
            next.prev = prev

        node.prev = None
        node.next = None

    def to_list(self) -> list[T]:
        out: list[T] = []
        cur = self.head
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out

    def to_reverse_list(self) -> list[T]:
        out: list[T] = []
        cur = self.tail
        while cur is not None:
            out.append(cur.value)
            cur = cur.prev
        return out

    def reverse(self) -> None:
        cur = self.head
        while cur is not None:
            cur.prev, cur.next = cur.next, cur.prev
            cur = cur.prev
        self.head, self.tail = self.tail, self.head

    def __len__(self) -> int:
        return self._size
