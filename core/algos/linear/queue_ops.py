from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.structures.linear.queue import OpKind, Queue


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    value: Any | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    queue: Queue[Any]
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

        if cmd == OpKind.ENQUEUE:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: 'enqueue' requiere un valor (ej: enqueue 10).")
            ops.append(Operation(kind="enqueue", value=_parse_value(parts[1])))
        elif cmd == OpKind.DEQUEUE:
            ops.append(Operation(kind="dequeue"))
        else:
            raise ValueError(f"Línea {i}: comando no válido '{parts[0]}'. Usa enqueue/dequeue.")
    return ops


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    q: Queue[Any] = Queue()
    steps: list[Step] = [
        Step(dot=dot_builder(q.to_list()), queue=q.to_list(), message="Estado inicial")
    ]

    for op in ops:
        if op.kind == OpKind.ENQUEUE:
            q.enqueue(op.value)
            steps.append(
                Step(dot=dot_builder(q.to_list()), queue=q.to_list(), message=f"enqueue {op.value}")
            )
        else:  # OpKind.DEQUEUE
            try:
                removed = q.dequeue()
                steps.append(
                    Step(
                        dot=dot_builder(q.to_list()),
                        queue=q.to_list(),
                        message=f"dequeue → {removed}",
                    )
                )
            except IndexError:
                steps.append(
                    Step(
                        dot=dot_builder(q.to_list()),
                        queue=q.to_list(),
                        message="ERROR: dequeue en cola vacía (se detuvo la simulación)",
                    )
                )
                break

    return steps
