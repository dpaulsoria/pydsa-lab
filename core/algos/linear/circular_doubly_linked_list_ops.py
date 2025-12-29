from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.linear.circular_doubly_linked_list import CircularDoublyLinkedList


class OpKind(StrEnum):
    PUSH_FRONT = "push_front"
    PUSH_BACK = "push_back"
    POP_FRONT = "pop_front"
    POP_BACK = "pop_back"
    DELETE = "delete"
    DELETE_ALL = "delete_all"
    FIND = "find"
    ROTATE_LEFT = "rotate_left"
    ROTATE_RIGHT = "rotate_right"


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


def _parse_int(token: str, *, line: int) -> int:
    try:
        return int(token)
    except ValueError as err:
        raise ValueError(f"Línea {line}: valor inválido '{token}'. Debe ser entero.") from err


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
                "Usa push_front/push_back/pop_front/pop_back/delete/delete_all/find/"
                "rotate_left/rotate_right."
            ) from err

        try:
            if kind in {
                OpKind.PUSH_FRONT,
                OpKind.PUSH_BACK,
                OpKind.DELETE,
                OpKind.DELETE_ALL,
                OpKind.FIND,
            }:
                ops.append(Operation(kind=kind, value=_parse_value(parts[1])))

            elif kind in {OpKind.ROTATE_LEFT, OpKind.ROTATE_RIGHT}:
                ops.append(Operation(kind=kind, value=_parse_int(parts[1], line=i)))

            else:  # POP_FRONT / POP_BACK
                ops.append(Operation(kind=kind))

        except IndexError as err:
            raise ValueError(f"Línea {i}: faltan argumentos para '{cmd}'.") from err

    return ops


def _clamp_hi(idx: int | None, n: int) -> int | None:
    if idx is None or n <= 0:
        return None
    if idx < 0:
        idx = 0
    if idx >= n:
        idx = n - 1
    return idx


Handler = Callable[[CircularDoublyLinkedList[Any], Operation], tuple[str, int | None]]


def _h_push_front(cdll: CircularDoublyLinkedList[Any], op: Operation) -> tuple[str, int | None]:
    cdll.push_front(op.value)
    return (f"push_front {op.value}", 0)


def _h_push_back(cdll: CircularDoublyLinkedList[Any], op: Operation) -> tuple[str, int | None]:
    cdll.push_back(op.value)
    return (f"push_back {op.value}", len(cdll) - 1)


def _h_pop_front(cdll: CircularDoublyLinkedList[Any], op: Operation) -> tuple[str, int | None]:
    removed = cdll.pop_front()
    return (f"pop_front → {removed}", 0 if len(cdll) else None)


def _h_pop_back(cdll: CircularDoublyLinkedList[Any], op: Operation) -> tuple[str, int | None]:
    removed = cdll.pop_back()
    return (f"pop_back → {removed}", len(cdll) - 1 if len(cdll) else None)


def _h_delete(cdll: CircularDoublyLinkedList[Any], op: Operation) -> tuple[str, int | None]:
    ok = cdll.delete(op.value)
    return (f"delete {op.value} → {'OK' if ok else 'NO ENCONTRADO'}", None)


def _h_delete_all(cdll: CircularDoublyLinkedList[Any], op: Operation) -> tuple[str, int | None]:
    count = cdll.delete_all(op.value)
    return (f"delete_all {op.value} → {count}", None)


def _h_find(cdll: CircularDoublyLinkedList[Any], op: Operation) -> tuple[str, int | None]:
    idx = cdll.find_index(op.value)
    msg = f"find {op.value} → {idx if idx is not None else 'NO ENCONTRADO'}"
    return (msg, _clamp_hi(idx, len(cdll)))


def _h_rotate_left(cdll: CircularDoublyLinkedList[Any], op: Operation) -> tuple[str, int | None]:
    k = int(op.value)
    cdll.rotate_left(k)
    return (f"rotate_left {k}", 0 if len(cdll) else None)


def _h_rotate_right(cdll: CircularDoublyLinkedList[Any], op: Operation) -> tuple[str, int | None]:
    k = int(op.value)
    cdll.rotate_right(k)
    return (f"rotate_right {k}", 0 if len(cdll) else None)


HANDLERS: dict[OpKind, Handler] = {
    OpKind.PUSH_FRONT: _h_push_front,
    OpKind.PUSH_BACK: _h_push_back,
    OpKind.POP_FRONT: _h_pop_front,
    OpKind.POP_BACK: _h_pop_back,
    OpKind.DELETE: _h_delete,
    OpKind.DELETE_ALL: _h_delete_all,
    OpKind.FIND: _h_find,
    OpKind.ROTATE_LEFT: _h_rotate_left,
    OpKind.ROTATE_RIGHT: _h_rotate_right,
}


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    cdll: CircularDoublyLinkedList[Any] = CircularDoublyLinkedList()

    def snap(msg: str, hi: int | None = None) -> Step:
        vals = cdll.to_list()
        return Step(dot=dot_builder(vals, highlight_index=hi), values=vals, message=msg)

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            msg, hi = HANDLERS[op.kind](cdll, op)
            steps.append(snap(msg, hi=hi))
        except (IndexError, ValueError) as e:
            steps.append(snap(f"ERROR: {e} (se detuvo la simulación)"))
            break

    return steps
