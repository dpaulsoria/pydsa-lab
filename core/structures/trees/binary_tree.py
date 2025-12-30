from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class BTNode(Generic[T]):
    value: T
    left: BTNode[T] | None = None
    right: BTNode[T] | None = None


class BinaryTree(Generic[T]):
    def __init__(self) -> None:
        self.root: BTNode[T] | None = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def clear(self) -> None:
        self.root = None
        self._size = 0

    def insert(self, value: T) -> None:
        """Inserta por nivel (level-order), llenando izq->der."""
        node = BTNode(value=value)
        if self.root is None:
            self.root = node
            self._size = 1
            return

        q: deque[BTNode[T]] = deque([self.root])
        while q:
            cur = q.popleft()
            if cur.left is None:
                cur.left = node
                self._size += 1
                return
            if cur.right is None:
                cur.right = node
                self._size += 1
                return
            q.append(cur.left)
            q.append(cur.right)

    def find(self, value: T) -> BTNode[T] | None:
        if self.root is None:
            return None
        q: deque[BTNode[T]] = deque([self.root])
        while q:
            cur = q.popleft()
            if cur.value == value:
                return cur
            if cur.left is not None:
                q.append(cur.left)
            if cur.right is not None:
                q.append(cur.right)
        return None

    def has(self, value: T) -> bool:
        if self.root is None:
            return False
        q: deque[BTNode[T]] = deque([self.root])
        while q:
            cur = q.popleft()
            if cur.value == value:
                return True
            if cur.left is not None:
                q.append(cur.left)
            if cur.right is not None:
                q.append(cur.right)
        return False

    def delete(self, value: T) -> bool:
        """
        Borra la primera ocurrencia (BFS).
        Estrategia típica de Binary Tree (no BST):
        - Encuentra target
        - Encuentra el nodo más profundo y a la derecha (último en BFS)
        - Copia su value en target y lo desconecta
        """
        if self.root is None:
            return False

        if self._size == 1:
            if self.root.value == value:
                self.clear()
                return True
            return False

        # BFS para encontrar target y también el último nodo + su parent
        target: BTNode[T] | None = None
        # target_parent: BTNode[T] | None = None

        last: BTNode[T] = self.root
        last_parent: BTNode[T] | None = None

        q: deque[tuple[BTNode[T], BTNode[T] | None]] = deque([(self.root, None)])

        while q:
            cur, parent = q.popleft()
            last = cur
            last_parent = parent

            if cur.value == value and target is None:
                target = cur
                # target_parent = parent

            if cur.left is not None:
                q.append((cur.left, cur))
            if cur.right is not None:
                q.append((cur.right, cur))

        if target is None:
            return False

        # Reemplazar value y quitar el "last"
        target.value = last.value

        if last_parent is None:
            # no debería pasar con size>1, pero por seguridad
            self.root = None
            self._size = 0
            return True

        if last_parent.left is last:
            last_parent.left = None
        elif last_parent.right is last:
            last_parent.right = None

        self._size -= 1
        return True

    # ---------- Traversals ----------
    """
    TREE:
              4
        2           6
    1       3   5       7

    INORDER: 1 2 3 4 5 6 7
    """

    def inorder(self) -> list[T]:
        out: list[T] = []

        def dfs(n: BTNode[T] | None) -> None:
            if n is None:
                return
            dfs(n.left)
            out.append(n.value)
            dfs(n.right)

        dfs(self.root)
        return out

    """
    TREE:
              4
        2           6
    1       3   5       7

    PREORDER: 4 2 1 3 6 5 7
    """

    def preorder(self) -> list[T]:
        out: list[T] = []

        def dfs(n: BTNode[T] | None) -> None:
            if n is None:
                return
            out.append(n.value)
            dfs(n.left)
            dfs(n.right)

        dfs(self.root)
        return out

    """
    TREE:
              4
        2           6
    1       3   5       7

    POSTORDER: 1 3 2 5 7 6 4
    """

    def postorder(self) -> list[T]:
        out: list[T] = []

        def dfs(n: BTNode[T] | None) -> None:
            if n is None:
                return
            dfs(n.left)
            dfs(n.right)
            out.append(n.value)

        dfs(self.root)
        return out

    """
    TREE:
              4
        2           6
    1       3   5       7

    BFS: 4 2 6 1 3 5 7
    """

    def level_order(self) -> list[T]:
        """BFS (level-order)"""
        if self.root is None:
            return []
        out: list[T] = []
        q: deque[BTNode[T]] = deque([self.root])
        while q:
            cur = q.popleft()
            out.append(cur.value)
            if cur.left is not None:
                q.append(cur.left)
            if cur.right is not None:
                q.append(cur.right)
        return out

    def levels(self) -> list[list[T]]:
        """Para UI/render: niveles como listas."""
        if self.root is None:
            return []
        res: list[list[T]] = []
        q: deque[BTNode[T]] = deque([self.root])
        while q:
            level_size = len(q)
            row: list[T] = []
            for _ in range(level_size):
                cur = q.popleft()
                row.append(cur.value)
                if cur.left is not None:
                    q.append(cur.left)
                if cur.right is not None:
                    q.append(cur.right)
            res.append(row)
        return res

    def snapshot(self) -> dict[str, object]:
        return {
            "size": self._size,
            "levels": self.levels(),
            "level_order": self.level_order(),
        }
