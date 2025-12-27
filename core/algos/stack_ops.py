from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from core.structures.stack import Stack

OpKind = Literal["push", "pop"]


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

        if cmd == "push":
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: 'push' requiere un valor (ej: push 10).")
            ops.append(Operation(kind="push", value=_parse_value(parts[1])))
        elif cmd == "pop":
            ops.append(Operation(kind="pop"))
        else:
            raise ValueError(f"Línea {i}: comando no válido '{parts[0]}'. Usa push/pop.")
    return ops


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    s: Stack[Any] = Stack()
    steps: list[Step] = [
        Step(dot=dot_builder(s.to_list()), stack=s.to_list(), message="Estado inicial")
    ]

    for op in ops:
        if op.kind == "push":
            s.push(op.value)
            steps.append(
                Step(dot=dot_builder(s.to_list()), stack=s.to_list(), message=f"push {op.value}")
            )
        else:  # pop
            try:
                removed = s.pop()
                steps.append(
                    Step(
                        dot=dot_builder(s.to_list()), stack=s.to_list(), message=f"pop → {removed}"
                    )
                )
            except IndexError:
                steps.append(
                    Step(
                        dot=dot_builder(s.to_list()),
                        stack=s.to_list(),
                        message="ERROR: pop en stack vacío (se detuvo la simulación)",
                    )
                )
                break

    return steps
