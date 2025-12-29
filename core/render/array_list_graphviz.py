from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from graphviz import Digraph


def array_list_to_dot(values: Sequence[Any], *, highlight_index: int | None = None) -> str:
    g = Digraph("array_list")
    g.attr(rankdir="LR")
    g.attr("node", shape="record")

    if not values:
        g.node("empty", "∅", shape="plaintext")
        return g.source

    # record label: |{idx|val}|{idx|val}|...
    cells = []
    for i, v in enumerate(values):
        cell = f"{{{i}|{v}}}"
        cells.append(cell)

    label = "|".join(cells)

    if highlight_index is None or not (0 <= highlight_index < len(values)):
        g.node("arr", label)
    else:
        # Truco simple: dibujar 2 nodos (izq / highlighted / der) para resaltar
        left = values[:highlight_index]
        mid = values[highlight_index : highlight_index + 1]
        right = values[highlight_index + 1 :]

        def mk(seq: Sequence[Any], offset: int) -> str:
            parts = [f"{{{offset + m}|{n}}}" for m, n in enumerate(seq)]
            return "|".join(parts) if parts else ""

        left2 = mk(left, 0)
        mid2 = mk(mid, highlight_index)
        right2 = mk(right, highlight_index + 1)

        if left2:
            g.node("L", left2)
        g.node("M", mid2, style="filled", fillcolor="lightyellow")
        if right2:
            g.node("R", right2)

        # Conectar en orden
        if left2:
            g.edge("L", "M")
        if right2:
            g.edge("M", "R")

    return g.source
