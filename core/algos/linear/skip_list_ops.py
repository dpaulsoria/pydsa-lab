from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.structures.linear.skip_list import OpKind, SkipList


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    value: Any
    level: int | None = None  # solo para insert


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

        if cmd == OpKind.INSERT:
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
            ops.append(Operation(kind="insert", value=val, level=lvl))

        elif cmd in {OpKind.DELETE, OpKind.SEARCH}:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: '{cmd}' requiere un valor.")
            ops.append(Operation(kind=cmd, value=_parse_value(parts[1])))

        else:
            raise ValueError(
                f"Línea {i}: comando no válido '{parts[0]}'. Usa insert/delete/search."
            )
    return ops


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    sl: SkipList[Any] = SkipList(max_level=6, p=0.5, seed=7)

    def levels_now() -> list[list[Any]]:
        return sl.levels_as_lists()

    steps: list[Step] = [
        Step(dot=dot_builder(levels_now()), levels=levels_now(), message="Estado inicial")
    ]

    for op in ops:
        if op.kind == OpKind.INSERT:
            ok = sl.insert(op.value, level=op.level)
            msg = f"insert {op.value}" + (f" {op.level}" if op.level is not None else "")
            msg += f" → {'OK' if ok else 'YA EXISTE'}"
            steps.append(Step(dot=dot_builder(levels_now()), levels=levels_now(), message=msg))

        elif op.kind == OpKind.DELETE:
            ok = sl.delete(op.value)
            msg = f"delete {op.value} → {'OK' if ok else 'NO ENCONTRADO'}"
            steps.append(Step(dot=dot_builder(levels_now()), levels=levels_now(), message=msg))

        else:  # OpKind.SEARCH
            found = sl.search(op.value)
            trace = sl.search_trace(op.value)

            # highlight se define en términos de (row_idx, value) donde row_idx es la fila top->bottom
            # nuestra traza viene en (lvl_interno, value) donde lvl_interno cuenta desde 0 (base)
            # convertimos: row_idx = (top_level - lvl_interno)
            top_level = sl.level
            highlight: set[tuple[int, Any]] = set()
            for lvl_internal, v in trace:
                row_idx = top_level - lvl_internal
                highlight.add((row_idx, v))

            msg = f"search {op.value} → {'FOUND' if found else 'NOT FOUND'}"
            steps.append(
                Step(
                    dot=dot_builder(levels_now(), highlight=highlight),
                    levels=levels_now(),
                    message=msg,
                )
            )

    return steps
