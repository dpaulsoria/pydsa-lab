from core.algos.array_list_ops import build_steps, parse_operations
from core.render.array_list_graphviz import array_list_to_dot


def test_array_list_ops() -> None:
    ops = parse_operations("append 1\nappend 2\ninsert 1 9\nget 2\n")
    steps = build_steps(ops, dot_builder=array_list_to_dot)
    assert "digraph" in steps[-1].dot
    assert steps[-1].values == [1, 9, 2]
