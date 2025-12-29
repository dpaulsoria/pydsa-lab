from core.algos.linear.linked_list_ops import build_steps, parse_operations
from core.render.linear.linked_list_graphviz import linked_list_to_dot


def test_linked_list_ops_basic() -> None:
    ops = parse_operations("append 1\nappend 2\nfind 2\n")
    steps = build_steps(ops, linked_list_to_dot)
    assert steps[-1].values == [1, 2]
    assert "digraph" in steps[-1].dot
