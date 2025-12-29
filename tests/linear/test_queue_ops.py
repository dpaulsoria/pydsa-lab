from core.algos.linear.queue_ops import build_steps, parse_operations
from core.render.linear.queue_graphviz import queue_to_dot


def test_queue_ops_basic() -> None:
    ops = parse_operations("enqueue 1\nenqueue 2\ndequeue\n")
    steps = build_steps(ops, dot_builder=queue_to_dot)
    assert steps[-1].values == [2]
    assert "digraph" in steps[-1].dot
