from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.linear.stack import Stack


class OpKind(StrEnum):
    PUSH = "push"
    POP = "pop"
    PEEK = "peek"
    CLEAR = "clear"


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    value: Any | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    stack: list[Any]
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
                f"Línea {i}: comando no válido '{parts[0]}'. Usa push/pop/peek/clear."
            ) from err

        if kind == OpKind.PUSH:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: 'push' requiere un valor (ej: push 10).")
            ops.append(Operation(kind=kind, value=_parse_value(parts[1])))
        else:
            ops.append(Operation(kind=kind))

    return ops


Handler = Callable[[Stack[Any], Operation], str]


def _h_push(s: Stack[Any], op: Operation) -> str:
    s.push(op.value)
    return f"push {op.value}"


def _h_pop(s: Stack[Any], op: Operation) -> str:
    v = s.pop()
    return f"pop → {v}"


def _h_peek(s: Stack[Any], op: Operation) -> str:
    v = s.peek()
    return f"peek → {v}"


def _h_clear(s: Stack[Any], op: Operation) -> str:
    s.clear()
    return "clear"


HANDLERS: dict[OpKind, Handler] = {
    OpKind.PUSH: _h_push,
    OpKind.POP: _h_pop,
    OpKind.PEEK: _h_peek,
    OpKind.CLEAR: _h_clear,
}


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    s: Stack[Any] = Stack()

    def snap(msg: str) -> Step:
        vals = s.to_list()
        return Step(dot=dot_builder(vals), stack=vals, message=msg)

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            msg = HANDLERS[op.kind](s, op)
            steps.append(snap(msg))
        except IndexError as e:
            steps.append(snap(f"ERROR: {e} (se detuvo la simulación)"))
            break

    return steps
