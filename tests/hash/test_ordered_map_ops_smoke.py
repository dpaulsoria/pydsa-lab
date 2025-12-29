from __future__ import annotations

from typing import Any

import pytest

from core.algos.hash.ordered_map_ops import build_steps, parse_operations


def _dot_builder(*_args: Any, **_kwargs: Any) -> str:
    return "digraph G { X -> Y }"


def test_ordered_map_ops_empty_and_invalid_parse() -> None:
    assert parse_operations("# comentario\n\n") == []

    with pytest.raises(ValueError):
        parse_operations("comando_que_no_existe\n")


def test_ordered_map_ops_build_steps_smoke() -> None:
    # Sin ops: al menos debe construir el estado inicial
    steps = build_steps([], capacity=8, dot_builder=_dot_builder)
    assert steps
    assert isinstance(steps[0].dot, str)
    assert isinstance(steps[0].message, str)
