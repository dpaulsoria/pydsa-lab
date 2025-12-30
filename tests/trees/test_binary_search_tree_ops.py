from __future__ import annotations

from core.algos.trees.binary_search_tree_ops import build_steps, parse_operations
from core.render.trees.binary_search_tree_graphviz import binary_search_tree_to_dot


def test_bst_ops_basic() -> None:
    ops = parse_operations("insert 2\ninsert 1\ninsert 3\ninorder\nsearch 3\ndelete 2\nbfs\n")
    steps = build_steps(ops, dot_builder=binary_search_tree_to_dot)

    # último snapshot: delete 2 y bfs
    last = steps[-1]
    assert last.values == [1, 3]  # inorder ordenado
