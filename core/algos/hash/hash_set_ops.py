from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.hash.hash_set import HashSet
from core.structures.hash.hash_table import stable_hash


class OpKind(StrEnum):
    ADD = "add"
    REMOVE = "remove"
    CONTAINS = "contains"
    CLEAR = "clear"


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    value: Any | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    buckets: list[list[Any]]
    values: list[Any]
    message: str


def _parse_value(tok: str) -> Any:
    try:
        return int(tok)
    except ValueError:
        return tok


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
                f"Línea {i}: comando inválido '{parts[0]}'. Usa add/remove/contains/clear."
            ) from err

        if kind in {OpKind.ADD, OpKind.REMOVE, OpKind.CONTAINS}:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: '{kind.value}' requiere un valor.")
            ops.append(Operation(kind=kind, value=_parse_value(parts[1])))
        else:
            ops.append(Operation(kind=kind))

    return ops


Handler = Callable[[HashSet[Any], Operation], str]


def _h_add(s: HashSet[Any], op: Operation) -> str:
    s.add(op.value)
    return f"add {op.value}"


def _h_remove(s: HashSet[Any], op: Operation) -> str:
    ok = s.remove(op.value)
    return f"remove {op.value} → {'OK' if ok else 'NO ENCONTRADO'}"


def _h_contains(s: HashSet[Any], op: Operation) -> str:
    ok = s.contains(op.value)
    return f"contains {op.value} → {ok}"


def _h_clear(s: HashSet[Any], op: Operation) -> str:
    # recrea internamente (simple)
    # si quieres un clear real, lo agregas en HashSet
    while len(s) > 0:
        # no tenemos pop en set; esto es solo para demo
        break
    return "clear (no-op)"


HANDLERS: dict[OpKind, Handler] = {
    OpKind.ADD: _h_add,
    OpKind.REMOVE: _h_remove,
    OpKind.CONTAINS: _h_contains,
    OpKind.CLEAR: _h_clear,
}


def build_steps(ops: list[Operation], capacity: int, dot_builder: callable) -> list[Step]:
    s: HashSet[Any] = HashSet(capacity=capacity)

    def snap(msg: str, hv: Any | None = None) -> Step:
        ss = s.snapshot()
        buckets = ss["buckets"]
        hb = None
        if hv is not None:
            hb = stable_hash(hv) % int(ss["capacity"])
        return Step(
            dot=dot_builder(buckets, highlight_bucket=hb, highlight_value=hv),
            buckets=buckets,
            values=s.to_list(),
            message=msg,
        )

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        hv = op.value
        msg = HANDLERS[op.kind](s, op)
        steps.append(snap(msg, hv=hv))

    return steps
