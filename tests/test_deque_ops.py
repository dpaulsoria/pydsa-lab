from core.algos.deque_ops import build_steps, parse_operations
from core.render.deque_graphviz import deque_to_dot


def test_deque_ops_basic() -> None:
    ops = parse_operations("push_back 1\npush_front 0\npop_back\n")
    steps = build_steps(ops, dot_builder=deque_to_dot)
    assert steps[-1].deque == [0]
    assert "digraph" in steps[-1].dot
