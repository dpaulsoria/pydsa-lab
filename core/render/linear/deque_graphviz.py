from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from graphviz import Digraph


def deque_to_dot(items: Sequence[Any]) -> str:
    g = Digraph("deque")
    g.attr(rankdir="LR")
    g.attr("node", shape="box")

    g.node("front", "FRONT", shape="plaintext")
    g.node("back", "BACK", shape="plaintext")

    prev = "front"
    for i, item in enumerate(items):
        node_id = f"n{i}"
        label = str(item)

        # resaltamos extremos (si existen)
        if i == 0 and len(items) == 1 or i == 0:
            g.node(node_id, label, style="filled", fillcolor="lightyellow")
        elif i == len(items) - 1:
            g.node(node_id, label, style="filled", fillcolor="lightcyan")
        else:
            g.node(node_id, label)

        g.edge(prev, node_id)
        prev = node_id

    g.edge(prev, "back")
    return g.source
