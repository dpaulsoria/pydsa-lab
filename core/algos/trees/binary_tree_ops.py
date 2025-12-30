from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Literal

from core.structures.trees.binary_tree import BinaryTree, BTNode


class OpKind(StrEnum):
    INSERT = "insert"
    DELETE = "delete"
    FIND = "find"
    HAS = "has"
    TRAVERSE = "traverse"
    CLEAR = "clear"


TraverseKind = Literal["inorder", "preorder", "postorder", "level"]


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    a: Any | None = None
    b: Any | None = None  # traverse kind


@dataclass(frozen=True)
class Step:
    dot: str
    levels: list[list[Any]]
    values: list[Any]
    message: str


def _parse_value(tok: str) -> Any:
    try:
        return int(tok)
    except ValueError:
        return tok


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
                f"Línea {i}: comando inválido '{parts[0]}'. "
                "Usa insert/delete/find/traverse/clear."
            ) from err

        if kind in {OpKind.INSERT, OpKind.DELETE, OpKind.FIND}:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: '{kind.value}' requiere un valor.")
            ops.append(Operation(kind=kind, a=_parse_value(parts[1])))

        elif kind == OpKind.TRAVERSE:
            if len(parts) < 2:
                raise ValueError(
                    f"Línea {i}: 'traverse' requiere tipo: inorder/preorder/postorder/level."
                )
            t = parts[1].lower()
            if t not in {"inorder", "preorder", "postorder", "level"}:
                raise ValueError(
                    f"Línea {i}: traverse inválido '{parts[1]}'. "
                    "Usa inorder/preorder/postorder/level."
                )
            ops.append(Operation(kind=kind, b=t))

        else:  # clear
            ops.append(Operation(kind=kind))

    return ops


Handler = Callable[[BinaryTree[Any], Operation], tuple[str, Any | None]]


def _h_insert(bt: BinaryTree[Any], op: Operation) -> tuple[str, Any | None]:
    bt.insert(op.a)
    return (f"insert {op.a}", op.a)


def _h_delete(bt: BinaryTree[Any], op: Operation) -> tuple[str, Any | None]:
    ok = bt.delete(op.a)
    return (f"delete {op.a} → {'OK' if ok else 'NO ENCONTRADO'}", op.a)


def _h_find(bt: BinaryTree[Any], op: Operation) -> tuple[str, Any | None]:
    ok = bt.find(op.a)
    return (f"find {op.a} → {ok}", op.a if ok else None)


def _h_has(bt: BinaryTree[Any], op: Operation) -> tuple[str, Any | None]:
    ok = bt.has(op.a)
    return (f"has {op.a} → {ok}", op.a if ok else None)


def _h_traverse(bt: BinaryTree[Any], op: Operation) -> tuple[str, Any | None]:
    kind = op.b
    if kind == "inorder":
        arr = bt.inorder()
    elif kind == "preorder":
        arr = bt.preorder()
    elif kind == "postorder":
        arr = bt.postorder()
    else:
        arr = bt.level_order()
    return (f"traverse {kind} → {arr}", None)


def _h_clear(bt: BinaryTree[Any], op: Operation) -> tuple[str, Any | None]:
    bt.clear()
    return ("clear", None)


HANDLERS: dict[OpKind, Handler] = {
    OpKind.INSERT: _h_insert,
    OpKind.DELETE: _h_delete,
    OpKind.FIND: _h_find,
    OpKind.HAS: _h_has,
    OpKind.TRAVERSE: _h_traverse,
    OpKind.CLEAR: _h_clear,
}


def build_steps(
    ops: list[Operation],
    *,
    dot_builder: Callable[[BTNode[Any] | None], str],
) -> list[Step]:
    bt: BinaryTree[Any] = BinaryTree()

    def snap(msg: str, highlight: Any | None = None) -> Step:
        s = bt.snapshot()
        levels = s["levels"]  # type: ignore[assignment]
        values = s["level_order"]  # type: ignore[assignment]
        return Step(
            dot=dot_builder(bt.root, highlight_value=highlight),  # type: ignore[arg-type]
            levels=levels,  # type: ignore[arg-type]
            values=values,  # type: ignore[arg-type]
            message=msg,
        )

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        msg, hi = HANDLERS[op.kind](bt, op)
        steps.append(snap(msg, highlight=hi))

    return steps
