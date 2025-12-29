from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.structures.linear.doubly_linked_list import DoublyLinkedList, OpKind


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
    # número si es int, si no string
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

        if cmd in {
            OpKind.PUSH_FRONT,
            OpKind.PUSH_BACK,
            OpKind.DELETE,
            OpKind.DELETE_ALL,
            OpKind.FIND_INDEX,
        }:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: '{cmd}' requiere un valor.")
            ops.append(Operation(kind=OpKind(cmd), value=_parse_value(parts[1])))

        elif cmd == OpKind.DELETE_AT:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: 'delete_at' requiere un índice (ej: delete_at 2).")
            try:
                idx = int(parts[1])
            except ValueError as err:
                raise ValueError(
                    f"Línea {i}: índice inválido '{parts[1]}'. Debe ser entero."
                ) from err
            ops.append(Operation(kind=OpKind.DELETE_AT, value=idx))

        elif cmd in {OpKind.POP_FRONT, OpKind.POP_BACK, OpKind.REVERSE}:
            ops.append(Operation(kind=OpKind(cmd)))

        else:
            raise ValueError(
                f"Línea {i}: comando no válido '{parts[0]}'. "
                "Usa push_front/push_back/pop_front/pop_back/delete/delete_all/delete_at/find/reverse."
            )

    return ops


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    dll: DoublyLinkedList[Any] = DoublyLinkedList()

    steps: list[Step] = [
        Step(dot=dot_builder(dll.to_list()), values=dll.to_list(), message="Estado inicial")
    ]

    for op in ops:
        try:
            if op.kind == OpKind.PUSH_FRONT:
                dll.push_front(op.value)
                steps.append(
                    Step(
                        dot=dot_builder(dll.to_list()),
                        values=dll.to_list(),
                        message=f"push_front {op.value}",
                    )
                )

            elif op.kind == OpKind.PUSH_BACK:
                dll.push_back(op.value)
                steps.append(
                    Step(
                        dot=dot_builder(dll.to_list()),
                        values=dll.to_list(),
                        message=f"push_back {op.value}",
                    )
                )

            elif op.kind == OpKind.POP_FRONT:
                removed = dll.pop_front()
                steps.append(
                    Step(
                        dot=dot_builder(dll.to_list()),
                        values=dll.to_list(),
                        message=f"pop_front → {removed}",
                    )
                )

            elif op.kind == OpKind.POP_BACK:
                removed = dll.pop_back()
                steps.append(
                    Step(
                        dot=dot_builder(dll.to_list()),
                        values=dll.to_list(),
                        message=f"pop_back → {removed}",
                    )
                )

            elif op.kind == OpKind.DELETE:
                ok = dll.delete(op.value)
                steps.append(
                    Step(
                        dot=dot_builder(dll.to_list()),
                        values=dll.to_list(),
                        message=f"delete {op.value} → {'OK' if ok else 'NO ENCONTRADO'}",
                    )
                )

            elif op.kind == OpKind.DELETE_ALL:
                count = dll.delete_all(op.value)
                steps.append(
                    Step(
                        dot=dot_builder(dll.to_list()),
                        values=dll.to_list(),
                        message=f"delete_all {op.value} → {count}",
                    )
                )

            elif op.kind == OpKind.DELETE_AT:
                removed = dll.delete_at(int(op.value))  # value es índice
                steps.append(
                    Step(
                        dot=dot_builder(dll.to_list()),
                        values=dll.to_list(),
                        message=f"delete_at {op.value} → {removed}",
                    )
                )

            elif op.kind == OpKind.FIND_INDEX:
                idx = dll.find_index(op.value)
                steps.append(
                    Step(
                        dot=dot_builder(dll.to_list(), highlight_index=idx),
                        values=dll.to_list(),
                        message=f"find {op.value} → {idx if idx is not None else 'NO ENCONTRADO'}",
                    )
                )

            else:  # OpKind.REVERSE
                dll.reverse()
                steps.append(
                    Step(dot=dot_builder(dll.to_list()), values=dll.to_list(), message="reverse")
                )

        except IndexError as e:
            steps.append(
                Step(
                    dot=dot_builder(dll.to_list()),
                    values=dll.to_list(),
                    message=f"ERROR: {e} (se detuvo la simulación)",
                )
            )
            break

    return steps
