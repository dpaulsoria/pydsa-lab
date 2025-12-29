from __future__ import annotations

from collections.abc import Sequence
from itertools import pairwise
from typing import Any

from graphviz import Digraph


def hash_set_to_dot(
    buckets: Sequence[Sequence[Any]],
    *,
    highlight_bucket: int | None = None,
    highlight_value: Any | None = None,
) -> str:
    g = Digraph("hash_set")
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
        for j, v in enumerate(bucket):
            n_id = f"n{i}_{j}"
            n_label = f"{v}"
            if highlight_value is not None and v == highlight_value:
                g.node(n_id, n_label, style="filled", fillcolor="lightgreen")
            else:
                g.node(n_id, n_label)
            g.edge(prev, n_id)
            prev = n_id

    # Conecta buckets en línea para que el gráfico quede ordenado
    if len(buckets) > 1:
        for a, b in pairwise(range(len(buckets))):
            g.edge(f"b{a}", f"b{b}", style="invis")

    return g.source
