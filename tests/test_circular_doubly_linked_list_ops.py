from core.algos.circular_doubly_linked_list_ops import build_steps, parse_operations
from core.render.circular_doubly_linked_list_graphviz import cdll_to_dot


def test_cdll_ops_basic() -> None:
    ops = parse_operations("push_back 1\npush_back 2\nrotate_left 1\npop_front\n")
    steps = build_steps(ops, dot_builder=cdll_to_dot)
    assert "digraph" in steps[-1].dot
    assert steps[-1].values == [1]
