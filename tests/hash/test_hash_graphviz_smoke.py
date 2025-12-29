from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any


def _find_to_dot(mod: object) -> Callable[..., str]:
    for name, val in vars(mod).items():
        if callable(val) and name.endswith("_to_dot"):
            return val  # type: ignore[return-value]
    raise AssertionError("No encontré ninguna función '*_to_dot' en el módulo")


def _call_to_dot(fn: Callable[..., str]) -> str:
    sig = inspect.signature(fn)
    args: list[Any] = []
    kwargs: dict[str, Any] = {}

    is_ordered_map = "ordered" in sig.parameters  # <- clave

    # armar args requeridos
    for p in sig.parameters.values():
        if p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
            continue
        if p.default is not p.empty:
            continue  # opcional

        if p.name in {"buckets", "table"}:
            if is_ordered_map:
                # buckets de (k, v)
                args.append([[("a", 1), ("b", 2)], [], [("c", 3)]])
            else:
                # buckets de valores
                args.append([[1, 2], [], [3]])

        elif p.name in {"ordered"}:
            args.append([("a", 1), ("b", 2), ("c", 3)])

        elif p.name in {"items", "pairs", "entries"}:
            args.append([("a", 1), ("b", 2)])

        elif p.name in {"levels", "rows"}:
            args.append([[1, 2, 3]])

        else:
            # fallback genérico
            args.append([[1]])

    # highlights opcionales típicos
    if "highlight_bucket" in sig.parameters:
        kwargs["highlight_bucket"] = 0
    if "highlight_value" in sig.parameters:
        kwargs["highlight_value"] = 2
    if "highlight_key" in sig.parameters:
        kwargs["highlight_key"] = "a"
    if "highlight" in sig.parameters:
        kwargs["highlight"] = {("a", 1)}
    if "capacity" in sig.parameters and "capacity" not in kwargs:
        kwargs["capacity"] = 8

    dot = fn(*args, **kwargs)
    assert isinstance(dot, str)
    assert "digraph" in dot or "graph" in dot
    return dot


def test_hash_set_graphviz_to_dot_smoke() -> None:
    import core.render.hash.hash_set_graphviz as mod

    fn = _find_to_dot(mod)
    _call_to_dot(fn)


def test_ordered_map_graphviz_to_dot_smoke() -> None:
    import core.render.hash.ordered_map_graphviz as mod

    fn = _find_to_dot(mod)
    _call_to_dot(fn)
