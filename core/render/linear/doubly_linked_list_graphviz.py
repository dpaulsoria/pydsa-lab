from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from graphviz import Digraph


def doubly_linked_list_to_dot(
    items: Sequence[Any],
    highlight_index: int | None = None,
) -> str:
    g = Digraph("doubly_linked_list")
    g.attr(rankdir="LR")
    g.attr("node", shape="box")

    # Etiquetas
    g.node("HEAD", "HEAD", shape="plaintext")
    g.node("TAIL", "TAIL", shape="plaintext")

    if not items:
        g.edge("HEAD", "TAIL")
        return g.source

    # Nodos
    for i, item in enumerate(items):
        node_id = f"n{i}"
        label = str(item)

        if highlight_index is not None and i == highlight_index:
            g.node(node_id, label, style="filled", fillcolor="lightyellow")
        else:
            g.node(node_id, label)

    # Conexiones HEAD -> primer nodo y último nodo -> TAIL
    g.edge("HEAD", "n0")
    g.edge(f"n{len(items) - 1}", "TAIL")

    # Enlaces doble dirección entre nodos
    for i in range(len(items) - 1):
        g.edge(f"n{i}", f"n{i+1}", dir="both")

    return g.source
