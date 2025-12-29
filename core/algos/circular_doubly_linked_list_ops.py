from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from core.structures.circular_doubly_linked_list import CircularDoublyLinkedList

OpKind = Literal[
    "push_front",
    "push_back",
    "pop_front",
    "pop_back",
    "delete",
    "delete_all",
    "find",
    "rotate_left",
    "rotate_right",
]


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

        if cmd in {"push_front", "push_back", "delete", "delete_all", "find"}:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: '{cmd}' requiere un valor.")
            ops.append(Operation(kind=cmd, value=_parse_value(parts[1])))

        elif cmd in {"rotate_left", "rotate_right"}:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: '{cmd}' requiere un entero (ej: rotate_left 2).")
            try:
                k = int(parts[1])
            except ValueError as err:
                raise ValueError(
                    f"Línea {i}: valor inválido '{parts[1]}'. Debe ser entero."
                ) from err
            ops.append(Operation(kind=cmd, value=k))

        elif cmd in {"pop_front", "pop_back"}:
            ops.append(Operation(kind=cmd))

        else:
            raise ValueError(
                f"Línea {i}: comando no válido '{parts[0]}'. "
                "Usa push_front/push_back/pop_front/pop_back/delete/delete_all/find/rotate_left/rotate_right."
            )

    return ops


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    cdll: CircularDoublyLinkedList[Any] = CircularDoublyLinkedList()

    def snap(highlight: int | None = None) -> Step:
        vals = cdll.to_list()
        return Step(dot=dot_builder(vals, highlight_index=highlight), values=vals, message="")

    steps: list[Step] = [
        Step(dot=dot_builder(cdll.to_list()), values=cdll.to_list(), message="Estado inicial")
    ]

    for op in ops:
        try:
            if op.kind == "push_front":
                cdll.push_front(op.value)
                steps.append(
                    Step(
                        dot=dot_builder(cdll.to_list()),
                        values=cdll.to_list(),
                        message=f"push_front {op.value}",
                    )
                )

            elif op.kind == "push_back":
                cdll.push_back(op.value)
                steps.append(
                    Step(
                        dot=dot_builder(cdll.to_list()),
                        values=cdll.to_list(),
                        message=f"push_back {op.value}",
                    )
                )

            elif op.kind == "pop_front":
                removed = cdll.pop_front()
                steps.append(
                    Step(
                        dot=dot_builder(cdll.to_list()),
                        values=cdll.to_list(),
                        message=f"pop_front → {removed}",
                    )
                )

            elif op.kind == "pop_back":
                removed = cdll.pop_back()
                steps.append(
                    Step(
                        dot=dot_builder(cdll.to_list()),
                        values=cdll.to_list(),
                        message=f"pop_back → {removed}",
                    )
                )

            elif op.kind == "delete":
                ok = cdll.delete(op.value)
                steps.append(
                    Step(
                        dot=dot_builder(cdll.to_list()),
                        values=cdll.to_list(),
                        message=f"delete {op.value} → {'OK' if ok else 'NO ENCONTRADO'}",
                    )
                )

            elif op.kind == "delete_all":
                count = cdll.delete_all(op.value)
                steps.append(
                    Step(
                        dot=dot_builder(cdll.to_list()),
                        values=cdll.to_list(),
                        message=f"delete_all {op.value} → {count}",
                    )
                )

            elif op.kind == "find":
                idx = cdll.find_index(op.value)
                steps.append(
                    Step(
                        dot=dot_builder(cdll.to_list(), highlight_index=idx),
                        values=cdll.to_list(),
                        message=f"find {op.value} → {idx if idx is not None else 'NO ENCONTRADO'}",
                    )
                )

            elif op.kind == "rotate_left":
                k = int(op.value)
                cdll.rotate_left(k)
                steps.append(
                    Step(
                        dot=dot_builder(cdll.to_list()),
                        values=cdll.to_list(),
                        message=f"rotate_left {k}",
                    )
                )

            else:  # rotate_right
                k = int(op.value)
                cdll.rotate_right(k)
                steps.append(
                    Step(
                        dot=dot_builder(cdll.to_list()),
                        values=cdll.to_list(),
                        message=f"rotate_right {k}",
                    )
                )

        except IndexError as e:
            steps.append(
                Step(
                    dot=dot_builder(cdll.to_list()),
                    values=cdll.to_list(),
                    message=f"ERROR: {e} (se detuvo la simulación)",
                )
            )
            break

    return steps
