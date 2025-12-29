from __future__ import annotations

from collections.abc import Sequence
from itertools import pairwise
from typing import Any

from graphviz import Digraph


def ordered_map_to_dot(
    buckets: Sequence[Sequence[tuple[Any, Any]]],
    ordered: Sequence[tuple[Any, Any]],
    *,
    highlight_bucket: int | None = None,
    highlight_key: Any | None = None,
) -> str:
    g = Digraph("ordered_map")
    g.attr(rankdir="LR")
    g.attr("node", shape="box")

    # --- Hash buckets (arriba)
    g.node("HASH", "HASH INDEX", shape="plaintext")
    for i, bucket in enumerate(buckets):
        b_id = f"b{i}"
        label = f"bucket {i}"
        if highlight_bucket == i:
            g.node(b_id, label, style="filled", fillcolor="lightyellow")
        else:
            g.node(b_id, label)
        g.edge("HASH", b_id, style="dotted")

        prev = b_id
        for j, (k, _v) in enumerate(bucket):
            n_id = f"h{i}_{j}"
            n_label = f"{k}"
            if highlight_key is not None and k == highlight_key:
                g.node(n_id, n_label, style="filled", fillcolor="lightgreen")
            else:
                g.node(n_id, n_label)
            g.edge(prev, n_id)
            prev = n_id

    # --- Ordered list (abajo)
    g.node("ORDER", "ORDER (insertion)", shape="plaintext")

    if not ordered:
        g.node("empty", "∅", shape="box")
        g.edge("ORDER", "empty")
        return g.source

    # Crea nodos en orden
    for i, (k, v) in enumerate(ordered):
        n_id = f"o{i}"
        n_label = f"{k} → {v}"
        if highlight_key is not None and k == highlight_key:
            g.node(n_id, n_label, style="filled", fillcolor="lightgreen")
        else:
            g.node(n_id, n_label)

    g.edge("ORDER", "o0")
    if len(ordered) > 1:
        for a, b in pairwise(range(len(ordered))):
            g.edge(f"o{a}", f"o{b}")

    return g.source
