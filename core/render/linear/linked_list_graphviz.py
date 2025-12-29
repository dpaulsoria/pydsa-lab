from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from graphviz import Digraph


def linked_list_to_dot(items: Sequence[Any], highlight_index: int | None = None) -> str:
    g = Digraph("linked_list")
    g.attr(rankdir="LR")
    g.attr("node", shape="box")

    # HEAD
    g.node("head", "HEAD", shape="plaintext")

    prev = "head"
    for i, item in enumerate(items):
        node_id = f"n{i}"
        label = str(item)

        if highlight_index is not None and i == highlight_index:
            g.node(node_id, label, style="filled", fillcolor="lightyellow")
        else:
            g.node(node_id, label)

        g.edge(prev, node_id)
        prev = node_id

    # NULL al final
    g.node("null", "NULL", shape="plaintext")
    g.edge(prev, "null")

    return g.source
