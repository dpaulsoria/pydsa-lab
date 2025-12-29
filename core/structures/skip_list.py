from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class SkipNode(Generic[T]):
    value: T | None
    forward: list[SkipNode[T] | None] = field(default_factory=list)


class SkipList(Generic[T]):
    def __init__(self, *, max_level: int = 6, p: float = 0.5, seed: int = 7) -> None:
        if max_level < 1:
            raise ValueError("max_level must be >= 1")
        if not (0.0 < p < 1.0):
            raise ValueError("p must be between 0 and 1")

        self.max_level = max_level
        self.p = p
        self._rnd = Random(seed)

        self.level = 0
        self._size = 0

        # Sentinel head (no value), with max_level+1 pointers (0..max_level)
        self.head: SkipNode[T] = SkipNode(value=None, forward=[None] * (max_level + 1))

    def __len__(self) -> int:
        return self._size

    def random_level(self) -> int:
        lvl = 0
        while self._rnd.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def search(self, value: T) -> bool:
        cur = self.head
        for lvl in range(self.level, -1, -1):
            while cur.forward[lvl] is not None and cur.forward[lvl].value < value:  # type: ignore[operator]
                cur = cur.forward[lvl]  # type: ignore[assignment]
        cur = cur.forward[0] or self.head
        return cur.value == value

    def search_trace(self, value: T) -> list[tuple[int, T]]:
        """
        Devuelve una traza (nivel, value_del_nodo_visitado) para visualizar el recorrido.
        """
        trace: list[tuple[int, T]] = []
        cur = self.head

        for lvl in range(self.level, -1, -1):
            while cur.forward[lvl] is not None and cur.forward[lvl].value < value:  # type: ignore[operator]
                cur = cur.forward[lvl]  # type: ignore[assignment]
                if cur.value is not None:
                    trace.append((lvl, cur.value))
        # Paso final en nivel 0 (candidato)
        nxt = cur.forward[0]
        if nxt is not None and nxt.value is not None:
            trace.append((0, nxt.value))
        return trace

    def insert(self, value: T, *, level: int | None = None) -> bool:
        update: list[SkipNode[T]] = [self.head] * (self.max_level + 1)
        cur = self.head

        for lvl in range(self.level, -1, -1):
            while cur.forward[lvl] is not None and cur.forward[lvl].value < value:  # type: ignore[operator]
                cur = cur.forward[lvl]  # type: ignore[assignment]
            update[lvl] = cur

        nxt = cur.forward[0]
        if nxt is not None and nxt.value == value:
            return False  # ya existe

        new_level = level if level is not None else self.random_level()
        if new_level < 0 or new_level > self.max_level:
            raise ValueError("level out of range")

        if new_level > self.level:
            for lvl in range(self.level + 1, new_level + 1):
                update[lvl] = self.head
            self.level = new_level

        node = SkipNode(value=value, forward=[None] * (new_level + 1))
        for lvl in range(new_level + 1):
            node.forward[lvl] = update[lvl].forward[lvl]
            update[lvl].forward[lvl] = node

        self._size += 1
        return True

    def delete(self, value: T) -> bool:
        update: list[SkipNode[T]] = [self.head] * (self.max_level + 1)
        cur = self.head

        for lvl in range(self.level, -1, -1):
            while cur.forward[lvl] is not None and cur.forward[lvl].value < value:  # type: ignore[operator]
                cur = cur.forward[lvl]  # type: ignore[assignment]
            update[lvl] = cur

        target = cur.forward[0]
        if target is None or target.value != value:
            return False

        for lvl in range(self.level + 1):
            if update[lvl].forward[lvl] != target:
                continue
            update[lvl].forward[lvl] = target.forward[lvl] if lvl < len(target.forward) else None

        while self.level > 0 and self.head.forward[self.level] is None:
            self.level -= 1

        self._size -= 1
        return True

    def levels_as_lists(self) -> list[list[T]]:
        """
        Retorna listas por nivel desde top->0, solo valores.
        """
        levels: list[list[T]] = []
        # recolectar en nivel 0 todos los valores en orden
        base: list[T] = []
        cur = self.head.forward[0]
        while cur is not None:
            base.append(cur.value)  # type: ignore[arg-type]
            cur = cur.forward[0]

        # para cada nivel, filtrar los que existen en ese nivel
        # (un nodo existe en nivel L si tiene forward con length > L)
        # reconstruimos recorriendo desde head por ese nivel
        for lvl in range(self.level, -1, -1):
            row: list[T] = []
            cur2 = self.head.forward[lvl]
            while cur2 is not None:
                row.append(cur2.value)  # type: ignore[arg-type]
                # avanzar por ese nivel
                cur2 = cur2.forward[lvl] if lvl < len(cur2.forward) else None
            levels.append(row)

        return levels
