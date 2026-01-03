from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from graphviz import Digraph

from core.structures.trees.avl_tree import AVLNode


def _h(n: AVLNode[Any] | None) -> int:
    return n.height if n is not None else 0


def _bf(n: AVLNode[Any] | None) -> int:
    if n is None:
        return 0
    return _h(n.left) - _h(n.right)


def avl_tree_to_dot(
    root: AVLNode[Any] | None,
    *,
    highlight: Iterable[Any] | None = None,
) -> str:
    """
    Render Graphviz para AVL.

    highlight:
      valores a resaltar (por ejemplo, la traza de búsqueda).
    """
    hi = set(highlight or [])
    g = Digraph("avl_tree")
    g.attr(rankdir="TB")
    g.attr("node", shape="circle")

    if root is None:
        g.node("empty", "∅", shape="plaintext")
        return g.source

    def add(n: AVLNode[Any]) -> None:
        nid = str(id(n))
        label = f"{n.value}\nh={n.height}\nbf={_bf(n)}"
        if n.value in hi:
            g.node(nid, label, style="filled", fillcolor="lightyellow")
        else:
            g.node(nid, label)

        # Izquierdo
        if n.left is not None:
            add(n.left)
            g.edge(nid, str(id(n.left)), label="L")
        else:
            null_id = f"nullL_{nid}"
            g.node(null_id, "∅", shape="plaintext")
            g.edge(nid, null_id, label="L", style="dashed")

        # Derecho
        if n.right is not None:
            add(n.right)
            g.edge(nid, str(id(n.right)), label="R")
        else:
            null_id = f"nullR_{nid}"
            g.node(null_id, "∅", shape="plaintext")
            g.edge(nid, null_id, label="R", style="dashed")

    add(root)
    return g.source
