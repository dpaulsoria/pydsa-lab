from __future__ import annotations

from typing import Any

import pytest

from core.algos.hash.hash_set_ops import build_steps, parse_operations


def _dot_builder(*_args: Any, **_kwargs: Any) -> str:
    return "digraph G { A -> B }"


def test_hash_set_ops_parse_and_build_steps() -> None:
    text = "\n".join(
        [
            "add 1",
            "add a",
            "contains 1",
            "remove 2",
            "clear",
        ]
    )
    ops = parse_operations(text)
    assert len(ops) == 5

    steps = build_steps(ops, capacity=8, dot_builder=_dot_builder)
    assert len(steps) == len(ops) + 1
    assert isinstance(steps[0].dot, str)
    assert steps[0].message.lower().startswith("estado")
    assert isinstance(steps[-1].dot, str)
    assert "digraph" in steps[-1].dot


def test_hash_set_ops_invalid_command_raises() -> None:
    with pytest.raises(ValueError):
        parse_operations("nope 1\n")
