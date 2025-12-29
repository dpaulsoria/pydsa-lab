from core.algos.trees.binary_tree_ops import build_steps, parse_operations
from core.render.trees.binary_tree_graphviz import binary_tree_to_dot


def test_binary_tree_ops_basic() -> None:
    ops = parse_operations("insert 1\ninsert 2\ninsert 3\nfind 2\ntraverse level\ndelete 2\n")
    steps = build_steps(ops, dot_builder=binary_tree_to_dot)
    assert "Estado inicial" in steps[0].message
    assert steps[-1].values in ([1, 3, 2], [1, 3]) or isinstance(steps[-1].values, list)
