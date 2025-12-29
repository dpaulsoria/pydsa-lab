from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from graphviz import Digraph


def stack_to_dot(items: Sequence[Any]) -> str:
    g = Digraph("stack")
    g.attr(rankdir="BT")  # base abajo, top arriba
    g.attr("node", shape="box")

    g.node("base", "STACK")

    prev = "base"
    for i, item in enumerate(items):
        node_id = f"n{i}"
        label = str(item)
        if i == len(items) - 1 and items:
            g.node(node_id, label, style="filled", fillcolor="lightyellow")
        else:
            g.node(node_id, label)
        g.edge(prev, node_id)
        prev = node_id

    return g.source
