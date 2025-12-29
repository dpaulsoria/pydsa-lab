from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any

from graphviz import Digraph

from core.structures.trees.binary_tree import BTNode


@dataclass(frozen=True)
class _N:
    node: BTNode[Any]
    id: str


def binary_tree_to_dot(
    root: BTNode[Any] | None,
    *,
    highlight_value: Any | None = None,
) -> str:
    g = Digraph("binary_tree")
    g.attr(rankdir="TB")
    g.attr("node", shape="circle")

    if root is None:
        g.node("EMPTY", "∅", shape="plaintext")
        return g.source

    q: deque[_N] = deque([_N(root, "n0")])
    seen: dict[int, str] = {id(root): "n0"}
    next_id = 1

    def _node_label(v: Any) -> str:
        return str(v)

    while q:
        cur = q.popleft()
        v = cur.node.value
        if highlight_value is not None and v == highlight_value:
            g.node(cur.id, _node_label(v), style="filled", fillcolor="lightyellow")
        else:
            g.node(cur.id, _node_label(v))

        for child, edge_label in ((cur.node.left, "L"), (cur.node.right, "R")):
            if child is None:
                # nodo fantasma para mantener forma
                null_id = f"{cur.id}_{edge_label}_null"
                g.node(null_id, "∅", shape="plaintext")
                g.edge(cur.id, null_id, label=edge_label, style="dotted")
                continue

            cid = seen.get(id(child))
            if cid is None:
                cid = f"n{next_id}"
                next_id += 1
                seen[id(child)] = cid
                q.append(_N(child, cid))

            g.edge(cur.id, cid, label=edge_label)

    return g.source
