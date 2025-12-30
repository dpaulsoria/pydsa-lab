from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class BSTNode(Generic[T]):
    value: T
    left: BSTNode[T] | None = None
    right: BSTNode[T] | None = None


class BinarySearchTree(Generic[T]):
    def __init__(self) -> None:
        self.root: BSTNode[T] | None = None
        self._size: int = 0

    # ---------- Basics ----------
    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return bool(self._size)

    def is_empty(self) -> bool:
        return self._size == 0

    def clear(self) -> None:
        self.root = None
        self._size = 0

    # ---------- Search ----------
    def contains(self, value: T) -> bool:
        """True si existe el valor en el BST."""
        return self._find_node(value) is not None

    def search_trace(self, value: T) -> list[T]:
        """
        Retorna el camino de búsqueda (valores visitados) hasta encontrar el value,
        o hasta que termine (None).
        """
        if self.root is None:
            return []

        cur = self.root
        trace: list[T] = []
        while cur is not None:
            trace.append(cur.value)
            if cur.value == value:
                return trace
            cur = cur.left if value < cur.value else cur.right
        return trace

    def min_value(self) -> T:
        """Mínimo del árbol (más a la izquierda)."""
        if self.root is None:
            raise ValueError("empty tree")

        return self._min_node(self.root).value

    def max_value(self) -> T:
        """Máximo del árbol (más a la derecha)."""
        if self.root is None:
            raise ValueError("empty tree")

        return self._max_node(self.root).value

    # ---------- Insert ----------
    def insert(self, value: T) -> bool:
        """
        Inserta value si no existe.
        Retorna True si insertó, False si ya existía.
        """
        node = BSTNode(value)
        if self.root is None:
            self.root = node
            self._size = 1
            return True

        cur = self.root
        while True:
            if value == cur.value:
                return False
            elif value < cur.value:
                if cur.left is None:
                    cur.left = node
                    self._size += 1
                    return True
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = node
                    self._size += 1
                    return True
                cur = cur.right

    # ---------- Delete ----------
    def delete(self, value: T) -> bool:
        """
        Elimina value si existe.
        Retorna True si eliminó, False si no estaba.
        """
        self.root, deleted = self._delete_rec(self.root, value)
        if deleted:
            self._size -= 1
        return deleted

    # helpers delete
    def _delete_rec(self, node: BSTNode[T] | None, value: T) -> tuple[BSTNode[T] | None, bool]:
        """
        Retorna (nuevo_subarbol, deleted)
        """
        if node is None:
            return None, False

        if value < node.value:  # type: ignore[operator]
            node.left, deleted = self._delete_rec(node.left, value)
            return node, deleted
        if value > node.value:  # type: ignore[operator]
            node.right, deleted = self._delete_rec(node.right, value)
            return node, deleted

        # found node
        if node.left is None and node.right is None:
            return None, True
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True

        # two children: replace with inorder successor (min on right)
        succ_parent = node
        succ = node.right
        while succ.left is not None:
            succ_parent = succ
            succ = succ.left

        node.value = succ.value

        # delete successor node
        if succ_parent is node:
            succ_parent.right, _ = self._delete_rec(succ_parent.right, succ.value)
        else:
            succ_parent.left, _ = self._delete_rec(succ_parent.left, succ.value)

        return node, True

    def _min_node(self, node: BSTNode[T]) -> BSTNode[T]:
        """Devuelve el nodo mínimo desde node."""
        if node.left is not None:
            return self._min_node(node.left)
        return node

    def _max_node(self, node: BSTNode[T]) -> BSTNode[T]:
        """Devuelve el nodo maximo desde node."""
        if node.right is not None:
            return self._max_node(node.right)
        return node

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

        def dfs(n: BSTNode[T] | None) -> None:
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

        def dfs(n: BSTNode[T] | None) -> None:
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

        def dfs(n: BSTNode[T] | None) -> None:
            if n is None:
                return
            dfs(n.left)
            dfs(n.right)
            out.append(n.value)

        dfs(self.root)
        return out

    def bfs(self) -> list[T]:
        """Level-order traversal (cola)."""
        if self.root is None:
            return []

        out: list[T] = []
        q: deque[BSTNode[T]] = deque([self.root])
        while q:
            cur = q.popleft()
            out.append(cur.value)
            if cur.left is not None:
                q.append(cur.left)
            if cur.right is not None:
                q.append(cur.right)
        return out

    # ---------- Utils ----------
    def _find_node(self, value: T) -> BSTNode[T] | None:
        if self.root is None:
            return None
        cur = self.root
        while cur is not None:
            if cur.value == value:
                return cur
            cur = cur.left if value < cur.value else cur.right
        return None

    def height(self) -> int:
        """
        Altura en nodos:
        - árbol vacío -> 0
        - 1 nodo -> 1
        """

        def h(n: BSTNode[T] | None) -> int:
            if n is None:
                return 0
            return 1 + max(h(n.left), h(n.right))

        return h(self.root)

    def is_valid_bst(self) -> bool:
        """Verifica que se cumple la propiedad BST en el árbol."""

        def ok(n: BSTNode[T] | None, low: T | None, high: T | None) -> bool:
            if n is None:
                return True
            if low is not None and n.value <= low:
                return False
            if high is not None and n.value >= high:
                return False
            return ok(n.left, low, n.value) and ok(n.right, n.value, high)

        return ok(self.root, None, None)

    def snapshot(self) -> dict[str, object]:
        return {
            "size": self._size,
            "inorder": self.inorder(),
            "preorder": self.preorder(),
            "postorder": self.postorder(),
            "bfs": self.bfs(),
        }
