from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from graphviz import Digraph

from core.structures.trees.binary_search_tree import BSTNode


def binary_search_tree_to_dot(
    root: BSTNode[Any] | None,
    *,
    highlight_values: Sequence[Any] | None = None,
    highlight_target: Any | None = None,
) -> str:
    g = Digraph("bst")
    g.attr(rankdir="TB")
    g.attr("node", shape="circle")

    hv = set(highlight_values or [])

    if root is None:
        g.node("empty", "∅", shape="plaintext")
        return g.source

    def node_id(prefix: str, n: BSTNode[Any]) -> str:
        return f"{prefix}_{id(n)}"

    def walk(n: BSTNode[Any]) -> None:
        nid = node_id("n", n)
        label = str(n.value)

        if highlight_target is not None and n.value == highlight_target:
            g.node(nid, label, style="filled", fillcolor="lightgreen")
        elif n.value in hv:
            g.node(nid, label, style="filled", fillcolor="lightyellow")
        else:
            g.node(nid, label)

        if n.left is not None:
            lid = node_id("n", n.left)
            walk(n.left)
            g.edge(nid, lid, label="L")
        if n.right is not None:
            rid = node_id("n", n.right)
            walk(n.right)
            g.edge(nid, rid, label="R")

    walk(root)
    return g.source
