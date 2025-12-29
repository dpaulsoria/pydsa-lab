from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.linear.linked_list import LinkedList


class OpKind(StrEnum):
    PUSH_FRONT = "push_front"
    APPEND = "append"
    DELETE = "delete"
    DELETE_ALL = "delete_all"
    DELETE_AT = "delete_at"
    FIND = "find"
    SEARCH = "search"
    REVERSE = "reverse"


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


def _parse_int(token: str, *, line: int, what: str) -> int:
    try:
        return int(token)
    except ValueError as err:
        raise ValueError(f"Línea {line}: {what} inválido '{token}'. Debe ser entero.") from err


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
                "Usa push_front/append/delete/delete_all/delete_at/find/search/reverse."
            ) from err

        try:
            if kind in {
                OpKind.PUSH_FRONT,
                OpKind.APPEND,
                OpKind.DELETE,
                OpKind.DELETE_ALL,
                OpKind.FIND,
                OpKind.SEARCH,
            }:
                ops.append(Operation(kind=kind, value=_parse_value(parts[1])))

            elif kind == OpKind.DELETE_AT:
                idx = _parse_int(parts[1], line=i, what="índice")
                ops.append(Operation(kind=kind, value=idx))

            else:  # REVERSE
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


Handler = Callable[[LinkedList[Any], Operation], tuple[str, int | None]]


def _h_push_front(ll: LinkedList[Any], op: Operation) -> tuple[str, int | None]:
    ll.push_front(op.value)
    return (f"push_front {op.value}", 0)


def _h_append(ll: LinkedList[Any], op: Operation) -> tuple[str, int | None]:
    ll.append(op.value)
    return (f"append {op.value}", len(ll) - 1)


def _h_delete(ll: LinkedList[Any], op: Operation) -> tuple[str, int | None]:
    ok = ll.delete(op.value)
    return (f"delete {op.value} → {'OK' if ok else 'NO ENCONTRADO'}", None)


def _h_delete_all(ll: LinkedList[Any], op: Operation) -> tuple[str, int | None]:
    count = ll.delete_all(op.value)
    return (f"delete_all {op.value} → {count}", None)


def _h_delete_at(ll: LinkedList[Any], op: Operation) -> tuple[str, int | None]:
    idx = int(op.value)
    removed = ll.delete_at(idx)
    return (f"delete_at {idx} → {removed}", _clamp_hi(idx, len(ll)))


def _h_find(ll: LinkedList[Any], op: Operation) -> tuple[str, int | None]:
    idx = ll.find_index(op.value)
    msg = f"find {op.value} → {idx if idx is not None else 'NO ENCONTRADO'}"
    return (msg, _clamp_hi(idx, len(ll)))


def _h_search(ll: LinkedList[Any], op: Operation) -> tuple[str, int | None]:
    node = ll.search(op.value)
    ok = node is not None
    return (f"search {op.value} → {ok}", ll.find_index(op.value) if ok else None)


def _h_reverse(ll: LinkedList[Any], op: Operation) -> tuple[str, int | None]:
    ll.reverse()
    return ("reverse", None)


HANDLERS: dict[OpKind, Handler] = {
    OpKind.PUSH_FRONT: _h_push_front,
    OpKind.APPEND: _h_append,
    OpKind.DELETE: _h_delete,
    OpKind.DELETE_ALL: _h_delete_all,
    OpKind.DELETE_AT: _h_delete_at,
    OpKind.FIND: _h_find,
    OpKind.SEARCH: _h_search,
    OpKind.REVERSE: _h_reverse,
}


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    ll: LinkedList[Any] = LinkedList()

    def snap(msg: str, hi: int | None = None) -> Step:
        vals = ll.to_list()
        return Step(dot=dot_builder(vals, highlight_index=hi), values=vals, message=msg)

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            msg, hi = HANDLERS[op.kind](ll, op)
            steps.append(snap(msg, hi=hi))
        except (IndexError, ValueError) as e:
            steps.append(snap(f"ERROR: {e} (se detuvo la simulación)"))
            break

    return steps
