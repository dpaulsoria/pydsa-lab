from __future__ import annotations

from collections.abc import Sequence
from itertools import pairwise
from typing import Any

from graphviz import Digraph


def cdll_to_dot(values: Sequence[Any], *, highlight_index: int | None = None) -> str:
    g = Digraph("cdll")
    g.attr(rankdir="LR")
    g.attr("node", shape="box")

    g.node("HEAD", "HEAD", shape="plaintext")

    if not values:
        g.node("EMPTY", "∅", shape="plaintext")
        g.edge("HEAD", "EMPTY")
        return g.source

    # nodos (orden empieza en head)
    for i, v in enumerate(values):
        node_id = f"n{i}"
        if i == 0:
            # head siempre resaltado
            g.node(node_id, str(v), style="filled", fillcolor="lightblue")
        elif highlight_index is not None and i == highlight_index:
            g.node(node_id, str(v), style="filled", fillcolor="lightyellow")
        else:
            g.node(node_id, str(v))

    g.edge("HEAD", "n0")

    # enlaces consecutivos (doble dirección)
    for a, b in pairwise(range(len(values))):
        g.edge(f"n{a}", f"n{b}", dir="both")

    # cerrar el ciclo: último <-> primero (dashed para que se note)
    if len(values) > 1:
        g.edge(f"n{len(values)-1}", "n0", dir="both", style="dashed")
    else:
        # 1 nodo: self-loop dashed
        g.edge("n0", "n0", style="dashed")

    return g.source
