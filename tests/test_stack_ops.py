from core.algos.stack_ops import build_steps, parse_operations
from core.render.stack_graphviz import stack_to_dot


def test_stack_ops_basic() -> None:
    ops = parse_operations("push 1\npush 2\npop\n")
    steps = build_steps(ops, dot_builder=stack_to_dot)
    assert steps[-1].stack == [1]
    assert "digraph" in steps[-1].dot
