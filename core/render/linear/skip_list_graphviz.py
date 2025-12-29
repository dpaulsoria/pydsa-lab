from __future__ import annotations

from collections.abc import Sequence
from itertools import pairwise
from typing import Any

from graphviz import Digraph


def skip_list_to_dot(
    levels_top_to_bottom: Sequence[Sequence[Any]],
    *,
    highlight: set[tuple[int, Any]] | None = None,
) -> str:
    """
    levels_top_to_bottom: [Lmax, ..., L0]
    highlight: {(level_index_en_entrada, value)} para colorear nodos visitados en búsqueda
    """
    highlight = highlight or set()

    g = Digraph("skiplist")
    g.attr(rankdir="LR")
    g.attr("node", shape="box")

    # cada fila es un nivel (0 = top row en el parámetro)
    for row_idx, row in enumerate(levels_top_to_bottom):
        with g.subgraph(name=f"cluster_level_{row_idx}") as sg:
            sg.attr(rank="same")
            sg.node(
                f"lvl_{row_idx}",
                f"Level {len(levels_top_to_bottom) - 1 - row_idx}",
                shape="plaintext",
            )

            prev = f"lvl_{row_idx}"
            for v in row:
                node_id = f"L{row_idx}_{v}"

                if (row_idx, v) in highlight:
                    sg.node(node_id, str(v), style="filled", fillcolor="lightyellow")
                else:
                    sg.node(node_id, str(v))

                sg.edge(prev, node_id)
                prev = node_id

    # conexiones verticales (mismo valor en niveles)
    # mapeo de dónde aparece cada valor (row_idx list)
    positions: dict[Any, list[int]] = {}
    for row_idx, row in enumerate(levels_top_to_bottom):
        for v in row:
            positions.setdefault(v, []).append(row_idx)

    for v, rows in positions.items():
        rows_sorted = sorted(rows)
        for a, b in pairwise(rows_sorted):
            g.edge(f"L{a}_{v}", f"L{b}_{v}", style="dashed", dir="none")

    return g.source
