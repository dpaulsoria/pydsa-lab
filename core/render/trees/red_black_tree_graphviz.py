from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from graphviz import Digraph

from core.structures.trees.red_black_tree import RBNode


def red_black_tree_to_dot(
    root: RBNode[Any] | None,
    *,
    highlight: Iterable[Any] | None = None,
) -> str:
    """
    Render Graphviz para LLRB.

    - Nodos rojos: fillcolor=lightcoral
    - Nodos negros: fillcolor=lightgray
    - highlight: valores a resaltar (ej: traza de búsqueda)
    """
    hi = set(highlight or [])
    g = Digraph("red_black_tree")
    g.attr(rankdir="TB")
    g.attr("node", shape="circle", style="filled")

    if root is None:
        g.node("empty", "∅", shape="plaintext", style="")
        return g.source

    def node_style(n: RBNode[Any]) -> dict[str, str]:
        if n.value in hi:
            return {"fillcolor": "lightyellow"}
        return {"fillcolor": "lightcoral" if n.red else "lightgray"}

    def add(n: RBNode[Any]) -> None:
        nid = str(id(n))
        color = "R" if n.red else "B"
        g.node(nid, f"{n.value}\n{color}", **node_style(n))

        # Left
        if n.left is not None:
            add(n.left)
            g.edge(nid, str(id(n.left)), label="L")
        else:
            null_id = f"nullL_{nid}"
            g.node(null_id, "∅", shape="plaintext", style="")
            g.edge(nid, null_id, label="L", style="dashed")

        # Right
        if n.right is not None:
            add(n.right)
            g.edge(nid, str(id(n.right)), label="R")
        else:
            null_id = f"nullR_{nid}"
            g.node(null_id, "∅", shape="plaintext", style="")
            g.edge(nid, null_id, label="R", style="dashed")

    add(root)
    return g.source
