from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class AVLNode(Generic[T]):
    """
    Nodo AVL.

    height:
      Altura en nodos (hoja = 1, None = 0).
      Se recalcula con _update_height() después de cambios.
    """

    value: T
    height: int = 1
    left: AVLNode[T] | None = None
    right: AVLNode[T] | None = None


class AVLTree(Generic[T]):
    """
    AVL Tree (BST auto-balanceado).

    Invariante AVL:
      Para todo nodo n, abs(balance_factor(n)) <= 1
      donde balance_factor(n) = height(left) - height(right)

    Garantiza:
      altura O(log n) => operaciones típicas O(log n).
    """

    def __init__(self) -> None:
        self.root: AVLNode[T] | None = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return bool(self._size)

    def is_empty(self) -> bool:
        return self._size == 0

    def clear(self) -> None:
        """Vacía el árbol en O(1)."""
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
        if inserted:
            self._size += 1
        return inserted

    def delete(self, value: T) -> bool:
        self.root, deleted = self._delete_rec(self.root, value)
        if deleted:
            self._size -= 1
        return deleted

    # TODO: Conseguir un ejemplo
    # DFS inorder (en un BST retorna ordenado)
    def inorder(self) -> list[T]:
        out: list[T] = []

        def dfs(n: AVLNode[T] | None) -> None:
            if n is None:
                return
            dfs(n.left)
            out.append(n.value)
            dfs(n.right)

        dfs(self.root)
        return out

    # DFS preorder
    def preorder(self) -> list[T]:
        out: list[T] = []

        def dfs(n: AVLNode[T] | None) -> None:
            if n is None:
                return
            out.append(n.value)
            dfs(n.left)
            dfs(n.right)

        dfs(self.root)
        return out

    # DFS postorder
    def postorder(self) -> list[T]:
        out: list[T] = []

        def dfs(n: AVLNode[T] | None) -> None:
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
        q: deque[AVLNode[T]] = deque([self.root])

        while q:
            cur = q.popleft()
            out.append(cur.value)
            if cur.left is not None:
                q.append(cur.left)
            if cur.right is not None:
                q.append(cur.right)
        return out

    def height(self) -> int:
        return self._h(self.root)

    def is_valid_avl(self) -> bool:
        """
        Verifica
        - Propiedad BST global
        - Altura almacenada correcta en cada nodo
        - Balance factor [-1, 1]
        """

        def check(n: AVLNode[T] | None, low: T | None, high: T | None) -> tuple[bool, int]:
            if n is None:
                return True, 0

            if low is not None and n.value <= low:
                return False, 0
            if high is not None and n.value >= high:
                return False, 0

            ok_left, high_left = check(n.left, low, n.value)
            if not ok_left:
                return False, 0

            ok_right, high_right = check(n.right, n.value, high)
            if not ok_right:
                return False, 0

            computed_h = 1 + max(high_left, high_right)
            bf = high_left - high_right

            if n.height != computed_h:
                return False, 0
            if bf < -1 or bf > 1:
                return False, 0

            return True, computed_h

        ok, _ = check(self.root, None, None)
        return ok

    def snapshot(self) -> dict[str, object]:
        return {
            "size": self._size,
            "height": self.height(),
            "inorder": self.inorder(),
            "preorder": self.preorder(),
            "postorder": self.postorder(),
            "bfs": self.bfs(),
        }

    def _h(self, n: AVLNode[T] | None) -> int:
        return n.height if n is not None else 0

    def _bf(self, n: AVLNode[T] | None) -> int:
        """Balance factor: height(left) - height(right)"""
        if n is None:
            return 0
        return self._h(n.left) - self._h(n.right)

    def _update_height(self, n: AVLNode[T]) -> None:
        """Recalculate the height from n"""
        n.height = 1 + max(self._h(n.left), self._h(n.right))

    def _rotate_right(self, y: AVLNode[T]) -> AVLNode[T]:
        """
        Rotate Right (casos LL / LR como parte del fix).

            y                x

          x   T3   =>      T1  y

        T1  T2               T2  T3
        """
        x = y.left
        assert x is not None
        t2 = x.right

        x.right = y
        y.left = t2

        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode[T]) -> AVLNode[T]:
        """
        Rotate Left (casos RR / RL).

          x                  y

        T1  y     =>       x  T3

          T2 T3          T1 T2
        """
        y = x.right
        assert y is not None
        t2 = y.left

        y.left = x
        x.right = t2

        self._update_height(y)
        self._update_height(x)
        return y

    def _rebalance(self, n: AVLNode[T]) -> AVLNode[T]:
        """Rebalance a modified node (insert/delete) in a subtree"""
        self._update_height(n)
        bf = self._bf(n)

        # Left heavy
        if bf > 1:
            left = n.left
            assert left is not None
            if self._bf(left) < 0:
                # LR -> First a Left Rotation
                n.left = self._rotate_left(left)
            return self._rotate_right(n)

        if bf < -1:
            right = n.right
            assert right is not None
            if self._bf(right) > 0:
                # RL -> First a Right Rotation
                n.right = self._rotate_right(right)
            return self._rotate_left(n)

        return n

    def _insert_rec(self, node: AVLNode[T] | None, value: T) -> tuple[AVLNode[T] | None, bool]:
        """
        Recursive Insert
        -> Rebalance (unwind)
        :returns (new_subtree, inserted)
        """
        if node is None:
            return AVLNode(value), True

        if value == node.value:
            return node, False

        if value < node.value:
            node.left, ins = self._insert_rec(node.left, value)
        else:
            node.right, ins = self._insert_rec(node.right, value)

        if not ins:
            return node, False

        return self._rebalance(node), True

    def _delete_rec(self, node: AVLNode[T] | None, value: T) -> tuple[AVLNode[T] | None, bool]:
        """
        Recursive Delete
        -> Rebalance (unwind)
        :returns (new_subtree, deleted)
        """

        if node is None:
            return None, False

        if value < node.value:
            node.left, deleted = self._delete_rec(node.left, value)
            if not deleted:
                return node, False
            return self._rebalance(node), True

        if value > node.value:
            node.right, deleted = self._delete_rec(node.right, value)
            if not deleted:
                return node, False
            return self._rebalance(node), True

        if node.left is None and node.right is None:
            return None, True

        if node.left is None:
            return node.right, True

        if node.right is None:
            return node.left, True

        # Two children: Replace with inorder successor (min on right)
        succ = self._min_node(node.right)
        node.value = succ.value
        node.right, _ = self._delete_rec(node.right, succ.value)
        return self._rebalance(node), True

    def _min_node(self, node: AVLNode[T]) -> AVLNode[T]:
        cur = node
        while cur.left is not None:
            cur = cur.left
        return cur

    def _max_node(self, node: AVLNode[T]) -> AVLNode[T]:
        cur = node
        while cur.right is not None:
            cur = cur.right
        return cur

    def _find_node(self, value: T) -> AVLNode[T] | None:
        """Iterative Search BST"""
        cur = self.root
        while cur is not None:
            if value == cur.value:
                return cur
            cur = cur.left if value < cur.value else cur.right
        return None
