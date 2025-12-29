from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.structures.stack import OpKind, Stack


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

        if cmd == OpKind.PUSH:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: 'push' requiere un valor (ej: push 10).")
            ops.append(Operation(kind=OpKind.PUSH, value=_parse_value(parts[1])))
        elif cmd == OpKind.POP:
            ops.append(Operation(kind=OpKind.POP))
        elif cmd == OpKind.PEEK:
            ops.append(Operation(kind=OpKind.PEEK))
        else:
            raise ValueError(f"Línea {i}: comando no válido '{parts[0]}'. Usa push/pop/peek.")
    return ops


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    s: Stack[Any] = Stack()
    steps: list[Step] = [
        Step(dot=dot_builder(s.to_list()), stack=s.to_list(), message="Estado inicial")
    ]

    for op in ops:
        if op.kind == OpKind.PUSH:
            s.push(op.value)
            steps.append(
                Step(dot=dot_builder(s.to_list()), stack=s.to_list(), message=f"push {op.value}")
            )

        elif op.kind == OpKind.POP:
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

        else:  # OpKind.PEEK
            top = s.peek()
            steps.append(
                Step(dot=dot_builder(s.to_list()), stack=s.to_list(), message=f"peek → {top}")
            )

    return steps
