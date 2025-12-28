from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from core.structures.deque_ds import DequeDS

OpKind = Literal["push_front", "push_back", "pop_front", "pop_back"]


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    value: Any | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    deque: list[Any]
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

        if cmd in {"push_front", "push_back"}:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: '{cmd}' requiere un valor.")
            ops.append(Operation(kind=cmd, value=_parse_value(parts[1])))
        elif cmd in {"pop_front", "pop_back"}:
            ops.append(Operation(kind=cmd))
        else:
            raise ValueError(
                f"Línea {i}: comando no válido '{parts[0]}'. "
                "Usa push_front/push_back/pop_front/pop_back."
            )
    return ops


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    d: DequeDS[Any] = DequeDS()
    steps: list[Step] = [
        Step(dot=dot_builder(d.to_list()), deque=d.to_list(), message="Estado inicial")
    ]

    for op in ops:
        if op.kind == "push_front":
            d.push_front(op.value)
            steps.append(
                Step(
                    dot=dot_builder(d.to_list()),
                    deque=d.to_list(),
                    message=f"push_front {op.value}",
                )
            )

        elif op.kind == "push_back":
            d.push_back(op.value)
            steps.append(
                Step(
                    dot=dot_builder(d.to_list()), deque=d.to_list(), message=f"push_back {op.value}"
                )
            )

        elif op.kind == "pop_front":
            try:
                removed = d.pop_front()
                steps.append(
                    Step(
                        dot=dot_builder(d.to_list()),
                        deque=d.to_list(),
                        message=f"pop_front → {removed}",
                    )
                )
            except IndexError:
                steps.append(
                    Step(
                        dot=dot_builder(d.to_list()),
                        deque=d.to_list(),
                        message="ERROR: pop_front en deque vacío (se detuvo la simulación)",
                    )
                )
                break

        else:  # pop_back
            try:
                removed = d.pop_back()
                steps.append(
                    Step(
                        dot=dot_builder(d.to_list()),
                        deque=d.to_list(),
                        message=f"pop_back → {removed}",
                    )
                )
            except IndexError:
                steps.append(
                    Step(
                        dot=dot_builder(d.to_list()),
                        deque=d.to_list(),
                        message="ERROR: pop_back en deque vacío (se detuvo la simulación)",
                    )
                )
                break

    return steps
