from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.render.linear.linked_list_graphviz import linked_list_to_dot
from core.structures.linear.linked_list import LinkedList, OpKind


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

        if cmd in {OpKind.PUSH_FRONT, OpKind.APPEND, OpKind.DELETE, OpKind.FIND_INDEX}:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: '{cmd}' requiere un valor.")
            ops.append(Operation(kind=cmd, value=_parse_value(parts[1])))
        else:
            raise ValueError(
                f"Línea {i}: comando no válido '{parts[0]}'. Usa push_front/append/delete/find."
            )
    return ops


def build_steps(ops: list[Operation]) -> list[Step]:
    ll: LinkedList[Any] = LinkedList()
    steps: list[Step] = [
        Step(dot=linked_list_to_dot(ll.to_list()), values=ll.to_list(), message="Estado inicial")
    ]

    for op in ops:
        if op.kind == OpKind.PUSH_FRONT:
            ll.push_front(op.value)
            steps.append(
                Step(
                    dot=linked_list_to_dot(ll.to_list()),
                    values=ll.to_list(),
                    message=f"push_front {op.value}",
                )
            )

        elif op.kind == OpKind.APPEND:
            ll.append(op.value)
            steps.append(
                Step(
                    dot=linked_list_to_dot(ll.to_list()),
                    values=ll.to_list(),
                    message=f"append {op.value}",
                )
            )

        elif op.kind == OpKind.DELETE:
            ok = ll.delete(op.value)
            msg = f"delete {op.value} → {'OK' if ok else 'NO ENCONTRADO'}"
            steps.append(
                Step(dot=linked_list_to_dot(ll.to_list()), values=ll.to_list(), message=msg)
            )

        else:  # OpKind.FIND_INDEX
            idx = ll.find_index(op.value)
            msg = f"find {op.value} → {idx if idx is not None else 'NO ENCONTRADO'}"
            steps.append(
                Step(
                    dot=linked_list_to_dot(ll.to_list(), highlight_index=idx),
                    values=ll.to_list(),
                    message=msg,
                )
            )

    return steps
