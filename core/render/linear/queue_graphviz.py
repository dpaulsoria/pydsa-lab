from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from graphviz import Digraph


def queue_to_dot(items: Sequence[Any]) -> str:
    g = Digraph("queue")
    g.attr(rankdir="LR")  # Left -> Right
    g.attr("node", shape="box")

    # Tags FRONT & BACK
    g.node("front", "FRONT", shape="plaintext")
    g.node("back", "BACK", shape="plaintext")

    prev = "front"

    for i, item in enumerate(items):
        node_id = f"n{i}"
        label = str(item)

        if i == 0:
            g.node(node_id, label, style="filled", fillcolor="lightyellow")
        else:
            g.node(node_id, label)

        g.edge(prev, node_id)
        prev = node_id

    g.edge(prev, "back")

    return g.source
