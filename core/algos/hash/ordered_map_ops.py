from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.hash.hash_table import stable_hash
from core.structures.hash.ordered_map import OrderedMap


class OpKind(StrEnum):
    SET = "set"
    GET = "get"
    DEL = "del"
    HAS = "has"


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    key: Any | None = None
    value: Any | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    buckets: list[list[tuple[Any, Any]]]
    ordered: list[tuple[Any, Any]]
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
                f"Línea {i}: comando inválido '{parts[0]}'. Usa set/get/del/has."
            ) from err

        if kind is OpKind.SET:
            if len(parts) < 3:
                raise ValueError(f"Línea {i}: set requiere: set key value")
            ops.append(
                Operation(kind=kind, key=_parse_value(parts[1]), value=_parse_value(parts[2]))
            )
        else:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: {kind.value} requiere: {kind.value} key")
            ops.append(Operation(kind=kind, key=_parse_value(parts[1])))

    return ops


Handler = Callable[[OrderedMap[Any, Any], Operation], str]


def _h_set(m: OrderedMap[Any, Any], op: Operation) -> str:
    m.set(op.key, op.value)
    return f"set {op.key} {op.value}"


def _h_get(m: OrderedMap[Any, Any], op: Operation) -> str:
    v = m.get(op.key)
    return f"get {op.key} → {v}"


def _h_del(m: OrderedMap[Any, Any], op: Operation) -> str:
    ok = m.delete(op.key)
    return f"del {op.key} → {'OK' if ok else 'NO ENCONTRADO'}"


def _h_has(m: OrderedMap[Any, Any], op: Operation) -> str:
    try:
        m.get(op.key)
        return f"has {op.key} → True"
    except KeyError:
        return f"has {op.key} → False"


HANDLERS: dict[OpKind, Handler] = {
    OpKind.SET: _h_set,
    OpKind.GET: _h_get,
    OpKind.DEL: _h_del,
    OpKind.HAS: _h_has,
}


def build_steps(ops: list[Operation], capacity: int, dot_builder: callable) -> list[Step]:
    m: OrderedMap[Any, Any] = OrderedMap(capacity=capacity)

    def snap(msg: str, hk: Any | None = None) -> Step:
        s = m.snapshot()
        cap = int(s["capacity"])
        hb = stable_hash(hk) % cap if hk is not None else None
        return Step(
            dot=dot_builder(s["buckets"], s["ordered"], highlight_bucket=hb, highlight_key=hk),
            buckets=s["buckets"],
            ordered=s["ordered"],
            message=msg,
        )

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            msg = HANDLERS[op.kind](m, op)
            steps.append(snap(msg, hk=op.key))
        except KeyError as e:
            steps.append(snap(f"ERROR: KeyError {e} (se detuvo la simulación)", hk=op.key))
            break

    return steps
