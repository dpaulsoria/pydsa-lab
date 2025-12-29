from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.linear.queue import Queue


class OpKind(StrEnum):
    ENQUEUE = "enqueue"
    DEQUEUE = "dequeue"
    FRONT = "front"
    IS_EMPTY = "is_empty"
    CLEAR = "clear"


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    value: Any | None = None


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
                "Usa enqueue/dequeue/front/is_empty/clear."
            ) from err

        try:
            if kind == OpKind.ENQUEUE:
                ops.append(Operation(kind=kind, value=_parse_value(parts[1])))
            else:
                ops.append(Operation(kind=kind))
        except IndexError as err:
            raise ValueError(f"Línea {i}: faltan argumentos para '{cmd}'.") from err

    return ops


Handler = Callable[[Queue[Any], Operation], str]


def _h_enqueue(q: Queue[Any], op: Operation) -> str:
    q.enqueue(op.value)
    return f"enqueue {op.value}"


def _h_dequeue(q: Queue[Any], op: Operation) -> str:
    removed = q.dequeue()
    return f"dequeue → {removed}"


def _h_front(q: Queue[Any], op: Operation) -> str:
    v = q.front()
    return f"front → {v}"


def _h_is_empty(q: Queue[Any], op: Operation) -> str:
    return f"is_empty → {q.is_empty()}"


def _h_clear(q: Queue[Any], op: Operation) -> str:
    q.clear()
    return "clear"


HANDLERS: dict[OpKind, Handler] = {
    OpKind.ENQUEUE: _h_enqueue,
    OpKind.DEQUEUE: _h_dequeue,
    OpKind.FRONT: _h_front,
    OpKind.IS_EMPTY: _h_is_empty,
    OpKind.CLEAR: _h_clear,
}


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    q: Queue[Any] = Queue()

    def snap(msg: str) -> Step:
        vals = q.to_list()
        return Step(dot=dot_builder(vals), values=vals, message=msg)

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            msg = HANDLERS[op.kind](q, op)
            steps.append(snap(msg))
        except (IndexError, ValueError) as e:
            steps.append(snap(f"ERROR: {e} (se detuvo la simulación)"))
            break

    return steps
