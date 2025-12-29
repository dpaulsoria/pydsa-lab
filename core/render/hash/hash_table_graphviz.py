from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from graphviz import Digraph


def hash_table_to_dot(
    buckets: Sequence[Sequence[tuple[Any, Any]]],
    *,
    highlight_bucket: int | None = None,
    highlight_key: Any | None = None,
) -> str:
    g = Digraph("hash_table")
    g.attr(rankdir="LR")
    g.attr("node", shape="box")

    for i, bucket in enumerate(buckets):
        b_id = f"b{i}"
        label = f"bucket {i}"
        if highlight_bucket == i:
            g.node(b_id, label, style="filled", fillcolor="lightyellow")
        else:
            g.node(b_id, label)

        prev = b_id
        for j, (k, v) in enumerate(bucket):
            n_id = f"n{i}_{j}"
            n_label = f"{k} → {v}"
            if highlight_key is not None and k == highlight_key:
                g.node(n_id, n_label, style="filled", fillcolor="lightgreen")
            else:
                g.node(n_id, n_label)
            g.edge(prev, n_id)
            prev = n_id

    return g.source
