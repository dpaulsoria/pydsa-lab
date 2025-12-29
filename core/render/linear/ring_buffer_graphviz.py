from __future__ import annotations

from collections.abc import Sequence
from itertools import pairwise
from typing import Any

from graphviz import Digraph


def ring_buffer_to_dot(
    buffer: Sequence[Any | None],
    *,
    head: int,
    tail: int,
    size: int,
) -> str:
    cap = len(buffer)
    g = Digraph("ring_buffer")
    g.attr(rankdir="LR")
    g.attr("node", shape="box")

    g.node("H", "HEAD", shape="plaintext")
    g.node("T", "TAIL", shape="plaintext")

    # índices activos (los que contienen elementos “vivos”)
    active: set[int] = set()
    if size > 0:
        idx = head
        for _ in range(size):
            active.add(idx)
            idx = (idx + 1) % cap

    for i, v in enumerate(buffer):
        label = f"{i}\\n{('∅' if v is None else v)}"

        # colores (prioridad: FULL(head==tail) > head > tail > active)
        if size == cap and head == tail and i == head:
            g.node(f"s{i}", label, style="filled", fillcolor="orange")
        elif size > 0 and i == head:
            g.node(f"s{i}", label, style="filled", fillcolor="lightgreen")
        elif i == tail:
            g.node(f"s{i}", label, style="filled", fillcolor="lightyellow")
        elif i in active:
            g.node(f"s{i}", label, style="filled", fillcolor="lightblue")
        else:
            g.node(f"s{i}", label)

    # conectar slots en línea
    if cap > 1:
        for a, b in pairwise(range(cap)):
            g.edge(f"s{a}", f"s{b}", dir="none")

    # punteros
    g.edge("H", f"s{head}")
    g.edge("T", f"s{tail}")

    return g.source
