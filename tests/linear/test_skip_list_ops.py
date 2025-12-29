from core.algos.linear.skip_list_ops import build_steps, parse_operations
from core.render.linear.skip_list_graphviz import skip_list_to_dot


def test_skip_list_ops_basic() -> None:
    ops = parse_operations("insert 10 2\ninsert 20 0\nsearch 20\ndelete 10\n")
    steps = build_steps(ops, dot_builder=skip_list_to_dot)

    assert "digraph" in steps[-1].dot
    assert "delete 10" in steps[-1].message
