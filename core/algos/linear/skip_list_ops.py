from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.linear.skip_list import SkipList


class OpKind(StrEnum):
    INSERT = "insert"
    DELETE = "delete"
    SEARCH = "search"


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    value: Any
    level: int | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    levels: list[list[Any]]  # top->bottom
    message: str


def _parse_value(token: str) -> Any:
    try:
        return int(token)
    except ValueError:
        return token


def parse_operations(text: str) -> list[Operation]:
    ops: list[Operation] = []
    for i, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        cmd = parts[0].lower()

        try:
            kind = OpKind(cmd)
        except ValueError as err:
            raise ValueError(
                f"Línea {i}: comando no válido '{parts[0]}'. Usa insert/delete/search."
            ) from err

        if kind == OpKind.INSERT:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: 'insert' requiere un valor.")
            val = _parse_value(parts[1])
            lvl: int | None = None
            if len(parts) >= 3:
                try:
                    lvl = int(parts[2])
                except ValueError as err:
                    raise ValueError(
                        f"Línea {i}: nivel inválido '{parts[2]}'. Debe ser entero."
                    ) from err
            ops.append(Operation(kind=kind, value=val, level=lvl))
            continue

        # delete/search
        if len(parts) < 2:
            raise ValueError(f"Línea {i}: '{kind.value}' requiere un valor.")
        ops.append(Operation(kind=kind, value=_parse_value(parts[1])))

    return ops


Handler = Callable[[SkipList[Any], Operation], tuple[str, set[tuple[int, Any]] | None]]


def _h_insert(sl: SkipList[Any], op: Operation) -> tuple[str, None]:
    ok = sl.insert(op.value, level=op.level)
    msg = f"insert {op.value}" + (f" {op.level}" if op.level is not None else "")
    msg += f" → {'OK' if ok else 'YA EXISTE'}"
    return msg, None


def _h_delete(sl: SkipList[Any], op: Operation) -> tuple[str, None]:
    ok = sl.delete(op.value)
    return f"delete {op.value} → {'OK' if ok else 'NO ENCONTRADO'}", None


def _h_search(sl: SkipList[Any], op: Operation) -> tuple[str, set[tuple[int, Any]]]:
    found = sl.search(op.value)
    trace = sl.search_trace(op.value)

    top_level = sl.level
    highlight: set[tuple[int, Any]] = set()
    for lvl_internal, v in trace:
        row_idx = top_level - lvl_internal  # top->bottom
        highlight.add((row_idx, v))

    msg = f"search {op.value} → {'FOUND' if found else 'NOT FOUND'}"
    return msg, highlight


HANDLERS: dict[OpKind, Handler] = {
    OpKind.INSERT: _h_insert,
    OpKind.DELETE: _h_delete,
    OpKind.SEARCH: _h_search,
}


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    sl: SkipList[Any] = SkipList(max_level=6, p=0.5, seed=7)

    def snap(msg: str, highlight: set[tuple[int, Any]] | None = None) -> Step:
        lvls = sl.levels_as_lists()
        return Step(dot=dot_builder(lvls, highlight=highlight), levels=lvls, message=msg)

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            msg, hi = HANDLERS[op.kind](sl, op)
            steps.append(snap(msg, highlight=hi))
        except (ValueError, IndexError) as e:
            steps.append(snap(f"ERROR: {e} (se detuvo la simulación)"))
            break

    return steps
