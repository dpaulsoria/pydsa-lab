from core.algos.hash.hash_table_ops import build_steps, parse_operations
from core.render.hash.hash_table_graphviz import hash_table_to_dot


def test_hash_ops_steps() -> None:
    ops = parse_operations("set a 1\nset b 2\nget a\ndelete b\n")
    steps = build_steps(ops, capacity=4, dot_builder=hash_table_to_dot)
    assert "digraph" in steps[-1].dot
