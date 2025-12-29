from core.algos.linear.ring_buffer_ops import build_steps, parse_operations
from core.render.linear.ring_buffer_graphviz import ring_buffer_to_dot


def test_rb_ops_builds_steps() -> None:
    ops = parse_operations("write 1\nwrite 2\nread\nwrite 3\npeek\n")
    steps = build_steps(ops, capacity=3, dot_builder=ring_buffer_to_dot)
    assert "digraph" in steps[-1].dot
    assert steps[-1].items == [2, 3]
