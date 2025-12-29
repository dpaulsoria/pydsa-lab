import pytest

from core.algos.doubly_linked_list_ops import build_steps, parse_operations
from core.render.doubly_linked_list_graphviz import doubly_linked_list_to_dot


def test_dll_ops_error_pop_empty_stops() -> None:
    ops = parse_operations("pop_front\npush_back 1\n")
    steps = build_steps(ops, dot_builder=doubly_linked_list_to_dot)
    assert "ERROR" in steps[-1].message
    assert steps[-1].values == []


def test_dll_ops_delete_all_delete_at_find_not_found_and_reverse() -> None:
    ops = parse_operations(
        "push_back 1\npush_back 2\npush_back 2\n"
        "delete_all 2\n"
        "find 99\n"
        "push_front 9\n"
        "reverse\n"
        "delete_at 0\n"
    )
    steps = build_steps(ops, dot_builder=doubly_linked_list_to_dot)
    # después de delete_all 2: queda [1]
    # push_front 9 -> [9,1]
    # reverse -> [1,9]
    # delete_at 0 -> elimina 1 -> [9]
    assert steps[-1].values == [9]


def test_dll_ops_invalid_command_raises() -> None:
    with pytest.raises(ValueError):
        parse_operations("enqueue 1\n")
