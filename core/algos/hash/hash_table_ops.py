from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from core.structures.hash.hash_table import HashTable, OpKind


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    key: Any | None = None
    value: Any | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    buckets: list[list[tuple[Any, Any]]]
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
                raise ValueError(f"Línea {i}: set requiere 2 args: set key value")
            ops.append(Operation(kind, _parse_value(parts[1]), _parse_value(parts[2])))
        else:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: {kind.value} requiere key: {kind.value} key")
            ops.append(Operation(kind, _parse_value(parts[1])))

    return ops


Handler = Callable[[HashTable[Any, Any], Operation], str]


def _h_set(ht: HashTable[Any, Any], op: Operation) -> str:
    ht.set(op.key, op.value)
    return f"set {op.key} {op.value}"


def _h_get(ht: HashTable[Any, Any], op: Operation) -> str:
    v = ht.get(op.key)
    return f"get {op.key} → {v}"


def _h_del(ht: HashTable[Any, Any], op: Operation) -> str:
    ok = ht.delete(op.key)
    return f"del {op.key} → {'OK' if ok else 'NO ENCONTRADO'}"


def _h_has(ht: HashTable[Any, Any], op: Operation) -> str:
    ok = ht.has(op.key)
    return f"has {op.key} → {ok}"


HANDLERS: dict[OpKind, Handler] = {
    OpKind.SET: _h_set,
    OpKind.GET: _h_get,
    OpKind.DELETE: _h_del,
    OpKind.HAS: _h_has,
}


def build_steps(ops: list[Operation], capacity: int, dot_builder: callable) -> list[Step]:
    ht: HashTable[Any, Any] = HashTable(capacity=capacity)

    def snap(msg: str, hb: int | None = None, hk: Any | None = None) -> Step:
        s = ht.snapshot()
        buckets = s["buckets"]
        return Step(
            dot=dot_builder(buckets, highlight_bucket=hb, highlight_key=hk),
            buckets=buckets,
            message=msg,
        )

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            hb = ht._index(op.key) if op.key is not None else None  # solo para resaltar
            msg = HANDLERS[op.kind](ht, op)
            steps.append(snap(msg, hb=hb, hk=op.key))
        except KeyError as e:
            steps.append(snap(f"ERROR: KeyError {e} (se detuvo la simulación)"))
            break

    return steps
