from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.linear.ring_buffer import RingBuffer


class OpKind(StrEnum):
    WRITE = "write"
    READ = "read"
    PEEK = "peek"
    CLEAR = "clear"
    WRITE_OVER = "write_over"


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    value: Any | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    buffer: list[Any | None]
    items: list[Any]
    head: int
    tail: int
    size: int
    capacity: int
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
                f"Línea {i}: comando no válido '{parts[0]}'. Usa write/read/peek/clear/write_over."
            ) from err

        if kind in {OpKind.WRITE, OpKind.WRITE_OVER}:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: '{kind.value}' requiere un valor.")
            ops.append(Operation(kind=kind, value=_parse_value(parts[1])))
        else:
            ops.append(Operation(kind=kind))

    return ops


Handler = Callable[[RingBuffer[Any], Operation], str]


def _h_write(rb: RingBuffer[Any], op: Operation) -> str:
    rb.write(op.value)
    return f"write {op.value}"


def _h_write_over(rb: RingBuffer[Any], op: Operation) -> str:
    rb.write_over(op.value)
    return f"write_over {op.value}"


def _h_read(rb: RingBuffer[Any], op: Operation) -> str:
    v = rb.read()
    return f"read → {v}"


def _h_peek(rb: RingBuffer[Any], op: Operation) -> str:
    v = rb.peek()
    return f"peek → {v}"


def _h_clear(rb: RingBuffer[Any], op: Operation) -> str:
    rb.clear()
    return "clear"


HANDLERS: dict[OpKind, Handler] = {
    OpKind.WRITE: _h_write,
    OpKind.WRITE_OVER: _h_write_over,
    OpKind.READ: _h_read,
    OpKind.PEEK: _h_peek,
    OpKind.CLEAR: _h_clear,
}


def build_steps(ops: list[Operation], capacity: int, dot_builder: callable) -> list[Step]:
    rb: RingBuffer[Any] = RingBuffer(capacity=capacity)

    def snap(msg: str) -> Step:
        s = rb.snapshot()
        return Step(
            dot=dot_builder(
                s["buffer"], head=int(s["head"]), tail=int(s["tail"]), size=int(s["size"])
            ),
            buffer=list(s["buffer"]),
            items=list(s["items"]),
            head=int(s["head"]),
            tail=int(s["tail"]),
            size=int(s["size"]),
            capacity=int(s["capacity"]),
            message=msg,
        )

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            msg = HANDLERS[op.kind](rb, op)
            steps.append(snap(msg))
        except (IndexError, OverflowError) as e:
            steps.append(snap(f"ERROR: {e} (se detuvo la simulación)"))
            break

    return steps
