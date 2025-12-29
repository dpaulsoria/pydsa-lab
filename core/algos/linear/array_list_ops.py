from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.linear.array_list import ArrayList


class OpKind(StrEnum):
    GET = "get"
    SET = "set"
    APPEND = "append"
    INSERT = "insert"
    POP = "pop"
    POP_AT = "pop_at"
    REMOVE_FIRST = "remove"
    CLEAR = "clear"


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    a: Any | None = None
    b: Any | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    values: list[Any]
    message: str


def _parse_value(token: str) -> Any:
    try:
        return int(token)
    except ValueError:
        return token


def _parse_int(token: str, *, line: int, what: str) -> int:
    try:
        return int(token)
    except ValueError as err:
        raise ValueError(f"Línea {line}: {what} inválido '{token}'. Debe ser entero.") from err


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
                f"Línea {i}: comando no válido '{parts[0]}'. "
                "Usa append/insert/pop/pop_at/remove/get/set/clear."
            ) from err

        try:
            match kind:
                case OpKind.APPEND:
                    ops.append(Operation(kind=kind, a=_parse_value(parts[1])))

                case OpKind.INSERT:
                    idx = _parse_int(parts[1], line=i, what="índice")
                    ops.append(Operation(kind=kind, a=idx, b=_parse_value(parts[2])))

                case OpKind.POP:
                    ops.append(Operation(kind=kind))

                case OpKind.POP_AT:
                    idx = _parse_int(parts[1], line=i, what="índice")
                    ops.append(Operation(kind=kind, a=idx))

                case OpKind.REMOVE_FIRST:
                    ops.append(Operation(kind=kind, a=_parse_value(parts[1])))

                case OpKind.GET:
                    idx = _parse_int(parts[1], line=i, what="índice")
                    ops.append(Operation(kind=kind, a=idx))

                case OpKind.SET:
                    idx = _parse_int(parts[1], line=i, what="índice")
                    ops.append(Operation(kind=kind, a=idx, b=_parse_value(parts[2])))

                case OpKind.CLEAR:
                    ops.append(Operation(kind=kind))

        except IndexError as err:
            raise ValueError(f"Línea {i}: faltan argumentos para '{cmd}'.") from err

    return ops


def _clamp_hi(idx: int | None, n: int) -> int | None:
    """Devuelve un highlight index seguro (o None)."""
    if n <= 0 or idx is None:
        return None
    if idx < 0:
        # Si alguien pasó -1, visualmente lo mandamos al último
        idx = n - 1
    if idx >= n:
        idx = n - 1
    return idx


Handler = Callable[[ArrayList[Any], Operation], tuple[str, int | None]]


def _h_append(arr: ArrayList[Any], op: Operation) -> tuple[str, int | None]:
    arr.append(op.a)
    return (f"append {op.a}", len(arr) - 1)


def _h_insert(arr: ArrayList[Any], op: Operation) -> tuple[str, int | None]:
    idx = int(op.a)
    arr.insert(idx, op.b)
    return (f"insert {idx} {op.b}", _clamp_hi(idx, len(arr)))


def _h_pop(arr: ArrayList[Any], op: Operation) -> tuple[str, int | None]:
    removed = arr.pop()
    return (f"pop → {removed}", len(arr) - 1 if len(arr) else None)


def _h_pop_at(arr: ArrayList[Any], op: Operation) -> tuple[str, int | None]:
    idx = int(op.a)
    removed = arr.pop_at(idx)
    return (f"pop_at {idx} → {removed}", _clamp_hi(idx, len(arr)))


def _h_remove(arr: ArrayList[Any], op: Operation) -> tuple[str, int | None]:
    ok = arr.remove_first(op.a)
    return (f"remove {op.a} → {'OK' if ok else 'NO ENCONTRADO'}", None)


def _h_get(arr: ArrayList[Any], op: Operation) -> tuple[str, int | None]:
    idx = int(op.a)
    val = arr.get(idx)
    return (f"get {idx} → {val}", _clamp_hi(idx, len(arr)))


def _h_set(arr: ArrayList[Any], op: Operation) -> tuple[str, int | None]:
    idx = int(op.a)
    arr.set(idx, op.b)
    return (f"set {idx} {op.b}", _clamp_hi(idx, len(arr)))


def _h_clear(arr: ArrayList[Any], op: Operation) -> tuple[str, int | None]:
    arr.clear()
    return ("clear", None)


HANDLERS: dict[OpKind, Handler] = {
    OpKind.APPEND: _h_append,
    OpKind.INSERT: _h_insert,
    OpKind.POP: _h_pop,
    OpKind.POP_AT: _h_pop_at,
    OpKind.REMOVE_FIRST: _h_remove,
    OpKind.GET: _h_get,
    OpKind.SET: _h_set,
    OpKind.CLEAR: _h_clear,
}


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    arr: ArrayList[Any] = ArrayList()

    def snap(msg: str, hi: int | None = None) -> Step:
        vals = arr.to_list()
        return Step(dot=dot_builder(vals, highlight_index=hi), values=vals, message=msg)

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            msg, hi = HANDLERS[op.kind](arr, op)
            steps.append(snap(msg, hi=hi))
        except (IndexError, ValueError) as e:
            steps.append(snap(f"ERROR: {e} (se detuvo la simulación)"))
            break

    return steps
