from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class RBNode(Generic[T]):
    """
    Node LLRB (Red-Black)

    red=True => red link
    red=False => black
    """

    value: T
    left: RBNode[T] | None = None
    right: RBNode[T] | None = None
    red: bool = True


class RedBlackTree(Generic[T]):
    """
    Red-Black Tree style LLRB (Left-Leaning Red-Black)

    - No reds on the right
    - No two consecutive reds (a red node cannot have a red child)
    - All ways root->None have the same quantity of black nodes
    - Property BST: left < node < right (without duplicates)
    """

    def __init__(self) -> None:
        self.root: RBNode[T] | None = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def is_empty(self) -> bool:
        return self._size == 0

    def clear(self) -> None:
        self.root = None
        self._size = 0

    def contains(self, value: T) -> bool:
        return self._find_node(value) is not None

    def search_trace(self, value: T) -> list[T]:
        trace: list[T] = []
        cur = self.root
        while cur is not None:
            trace.append(cur.value)
            if cur.value == value:
                return trace
            cur = cur.left if value < cur.value else cur.right
        return trace

    def min_value(self) -> T:
        if self.root is None:
            raise ValueError("Empty tree")
        return self._min_node(self.root).value

    def max_value(self) -> T:
        if self.root is None:
            raise ValueError("Empty tree")
        return self._max_node(self.root).value

    def insert(self, value: T) -> bool:
        self.root, inserted = self._insert_rec(self.root, value)
        if self.root is not None:
            self.root.red = False
        if inserted:
            self._size += 1
        return inserted

    def delete(self, value: T) -> bool:
        if self.root is None:
            return False
        if not self.contains(value):
            return False

        # If both children of root are black, then temporarily set root to red
        # To facilitate the "move_red_*" on the descent
        if not self._is_red(self.root.left) and not self.is_red(self.root.right):
            self.root.red = True

        self.root = self._delete_rec(self.root, value)
        if self.root is not None:
            self.root.red = False

        self._size -= 1
        return True

    def inorder(self) -> list[T]:
        out: list[T] = []

        def dfs(n: RBNode[T] | None) -> None:
            if n is None:
                return
            dfs(n.left)
            out.append(n.value)
            dfs(n.right)

        dfs(self.root)
        return out

    def preorder(self) -> list[T]:
        out: list[T] = []

        def dfs(n: RBNode[T] | None) -> None:
            if n is None:
                return
            out.append(n.value)
            dfs(n.left)
            dfs(n.right)

        dfs(self.root)
        return out

    def postorder(self) -> list[T]:
        out: list[T] = []

        def dfs(n: RBNode[T] | None) -> None:
            if n is None:
                return
            dfs(n.left)
            dfs(n.right)
            out.append(n.value)

        dfs(self.root)
        return out

    def bfs(self) -> list[T]:
        if self.root is None:
            return []

        out: list[T] = []
        q: deque[RBNode[T]] = deque([self.root])

        while q:
            cur = q.popleft()
            out.append(cur.value)
            if cur.left is not None:
                q.append(cur.left)
            if cur.right is not None:
                q.append(cur.right)
        return out

    def height(self) -> int:
        def h(n: RBNode[T] | None) -> int:
            return 0 if n is None else max(h(n.left), h(n.right)) + 1

        return h(self.root)

    def is_valid_llrb(self) -> bool:
        """
        Validate:
        - BST Global
        - No red-right
        - No two-reds in a row
        - Black-height consistency
        - Root black (if exists)
        """
        if self.root is None:
            return True
        if self.root.red:
            return False

        # BST + red rules
        def check_rules(n: RBNode[T] | None, low: T | None, high: T | None) -> bool:
            if n is None:
                return True
            if low is not None and n.value <= low:
                return False
            if high is not None and n.value >= high:
                return False

            # No reds on the right
            if self._is_red(n.right):
                return False

            # No two consecutive reds (a red node cannot have a red child)
            if self.is_red(n) and (self._is_red(n.left) or self._is_red(n.right)):
                return False

            return check_rules(n.left, low, n.value) and check_rules(n.right, n.value, high)

        if not check_rules(self.root, None, None):
            return False

        def black_height(n: RBNode[T] | None) -> int:
            if n is None:
                return 1
            lh = black_height(n.left)
            rh = black_height(n.right)
            return -1 if lh == -1 or rh == -1 or lh != rh else lh + (0 if n.red else 1)

        return black_height(self.root) != -1

    def snapshot(self) -> dict[str, object]:
        return {
            "size": self._size,
            "height": self.height(),
            "inorder": self.inorder(),
            "preorder": self.preorder(),
            "postorder": self.postorder(),
            "bfs": self.bfs(),
        }

    def _is_red(self, n: RBNode[T] | None) -> bool:
        return n is not None and n.red

    def _rotate_left(self, h: RBNode[T]) -> RBNode[T]:
        """
        Fix red to the right
            h                 x
          a   x     =>      h   c
            b   c         a   b
        """
        x = h.right
        assert x is not None
        h.right = x.left
        x.left = h
        x.red = h.red
        h.red = True
        return x

    def _rotate_right(self, h: RBNode[T]) -> RBNode[T]:
        """
        Fix two reds to the left
              h              x
            x   c   =>     a   h
          a   b              b   c
        """
        x = h.left
        assert x is not None
        h.left = x.right
        x.right = h
        x.red = h.red
        h.red = True
        return x

    def _flip_colors(self, h: RBNode[T]) -> None:
        """Split/Merge four nodes (toggle)"""
        h.red = not h.red
        if h.left is not None:
            h.left.red = not h.left.red
        if h.right is not None:
            h.right.red = not h.right.red

    def _fix_up(self, h: RBNode[T]) -> RBNode[T]:
        """Normalize a subtree to hold the LLRB properties"""
        if self._is_red(h.right) and not self._is_red(h.left):
            h = self._rotate_left(h)
        if self._is_red(h.left) and self._is_red(h.left.left if h.left else None):
            h = self._rotate_right(h)
        if self._is_red(h.left) and self._is_red(h.right):
            self._flip_colors(h)
        return h

    def _move_red_left(self, h: RBNode[T]) -> RBNode[T]:
        """
        Move red links to the left
        Ensures an available red on the left
        """
        self._flip_colors(h)
        if h.right is not None and self._is_red(h.right.left):
            h.right = self._rotate_right(h.right)
            h = self._rotate_left(h)
            self._flip_colors(h)

        return h

    def _move_red_right(self, h: RBNode[T]) -> RBNode[T]:
        """
        Ensures an available red on the right
        """
        self._flip_colors(h)
        if h.left is not None and self._is_red(h.left.left):
            h = self._rotate_right(h)
            self._flip_colors(h)
        return h

    def _insert_rec(self, h: RBNode[T] | None, value: T) -> tuple[RBNode[T], bool]:
        """Recursive insert LLRB"""
        if h is None:
            return RBNode(value=value, red=True), True

        if value == h.value:
            return h, False

        if value < h.value:
            h.left, ins = self._insert_rec(h.left, value)
        else:
            h.right, ins = self._insert_rec(h.right, value)

        return self._fix_up(h), ins

    def _delete_min(self, h: RBNode[T]) -> RBNode[T] | None:
        """Delete the minimum value from subtree h"""
        if h.left is None:
            return None

        if not self._is_red(h.left) and not self._is_red(h.left.left):
            h = self._move_red_left(h)

        assert h.left is not None
        h.left = self._delete_min(h.left)
        return self._fix_up(h)

    def _delete_rec(self, h: RBNode[T] | None, value: T) -> RBNode[T] | None:
        """Recursive delete LLRB (assumes value exists)"""
        if h is None:
            return None

        if value < h.value and h.left is not None:
            if not self._is_red(h.left) and self._is_red(h.left.left):
                h = self._move_red_left(h)
            h.left = self._delete_rec(h.left, value)
        else:
            if self._is_red(h.left):
                h = self._rotate_right(h)

            if value == h.value and h.right is None:
                return None

            if h.right is not None:
                if not self._is_red(h.right) and not self._is_red(h.right.left):
                    h = self._move_red_right(h)

                if value == h.value:
                    m = self._min_node(h.right)
                    h.value = m.value
                    h.right = self._delete_min(h.right)
                else:
                    h.right = self._delete_rec(h.right, value)

        return self._fix_up(h)

    def _min_node(self, n: RBNode[T]) -> RBNode[T]:
        cur = n
        while cur.left is not None:
            cur = cur.left
        return cur

    def _max_node(self, n: RBNode[T]) -> RBNode[T]:
        cur = n
        while cur.right is not None:
            cur = cur.right
        return cur

    def _find_node(self, value: T) -> RBNode[T] | None:
        cur = self.root
        while cur is not None:
            if value == cur.value:
                return cur
            cur = cur.left if value < cur.value else cur.right
        return None
