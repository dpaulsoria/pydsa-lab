from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.linear.deque_ds import DequeDS


class OpKind(StrEnum):
    PUSH_FRONT = "push_front"
    PUSH_BACK = "push_back"
    POP_FRONT = "pop_front"
    POP_BACK = "pop_back"
    PEEK_FRONT = "peek_front"
    PEEK_BACK = "peek_back"
    IS_EMPTY = "is_empty"
    CLEAR = "clear"


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

        try:
            kind = OpKind(cmd)
        except ValueError as err:
            raise ValueError(
                f"Línea {i}: comando no válido '{parts[0]}'. "
                "Usa push_front/push_back/pop_front/pop_back/peek_front/peek_back/is_empty/clear."
            ) from err

        try:
            match kind:
                case OpKind.PUSH_FRONT | OpKind.PUSH_BACK:
                    ops.append(Operation(kind=kind, value=_parse_value(parts[1])))

                case (
                    OpKind.POP_FRONT
                    | OpKind.POP_BACK
                    | OpKind.PEEK_FRONT
                    | OpKind.PEEK_BACK
                    | OpKind.IS_EMPTY
                    | OpKind.CLEAR
                ):
                    ops.append(Operation(kind=kind))

        except IndexError as err:
            raise ValueError(f"Línea {i}: faltan argumentos para '{cmd}'.") from err

    return ops


Handler = Callable[[DequeDS[Any], Operation], str]


def _h_push_front(d: DequeDS[Any], op: Operation) -> str:
    d.push_front(op.value)
    return f"push_front {op.value}"


def _h_push_back(d: DequeDS[Any], op: Operation) -> str:
    d.push_back(op.value)
    return f"push_back {op.value}"


def _h_pop_front(d: DequeDS[Any], op: Operation) -> str:
    removed = d.pop_front()
    return f"pop_front → {removed}"


def _h_pop_back(d: DequeDS[Any], op: Operation) -> str:
    removed = d.pop_back()
    return f"pop_back → {removed}"


def _h_peek_front(d: DequeDS[Any], op: Operation) -> str:
    v = d.peek_front()
    return f"peek_front → {v}"


def _h_peek_back(d: DequeDS[Any], op: Operation) -> str:
    v = d.peek_back()
    return f"peek_back → {v}"


def _h_is_empty(d: DequeDS[Any], op: Operation) -> str:
    return f"is_empty → {d.is_empty()}"


def _h_clear(d: DequeDS[Any], op: Operation) -> str:
    d.clear()
    return "clear"


HANDLERS: dict[OpKind, Handler] = {
    OpKind.PUSH_FRONT: _h_push_front,
    OpKind.PUSH_BACK: _h_push_back,
    OpKind.POP_FRONT: _h_pop_front,
    OpKind.POP_BACK: _h_pop_back,
    OpKind.PEEK_FRONT: _h_peek_front,
    OpKind.PEEK_BACK: _h_peek_back,
    OpKind.IS_EMPTY: _h_is_empty,
    OpKind.CLEAR: _h_clear,
}


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    d: DequeDS[Any] = DequeDS()

    def snap(msg: str) -> Step:
        vals = d.to_list()
        return Step(dot=dot_builder(vals), deque=vals, message=msg)

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            msg = HANDLERS[op.kind](d, op)
            steps.append(snap(msg))
        except (IndexError, ValueError) as e:
            steps.append(snap(f"ERROR: {e} (se detuvo la simulación)"))
            break

    return steps
