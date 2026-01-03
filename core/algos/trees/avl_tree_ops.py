from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.trees.avl_tree import AVLTree


class OpKind(StrEnum):
    INSERT = "insert"
    DELETE = "delete"
    CONTAINS = "contains"
    TRACE = "trace"
    INORDER = "inorder"
    BFS = "bfs"
    CLEAR = "clear"


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    value: Any | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    inorder: list[Any]
    bfs: list[Any]
    height: int
    message: str


def _parse_value(tok: str) -> Any:
    try:
        return int(tok)
    except ValueError:
        return tok


def parse_operations(text: str) -> list[Operation]:
    """
    Gramática (una por línea):
      insert X
      delete X
      contains X
      trace X
      inorder
      bfs
      clear
    """
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
                "Usa insert/delete/contains/trace/inorder/bfs/clear."
            ) from err

        if kind in {OpKind.INSERT, OpKind.DELETE, OpKind.CONTAINS, OpKind.TRACE}:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: '{kind.value}' requiere un valor.")
            ops.append(Operation(kind=kind, value=_parse_value(parts[1])))
        else:
            ops.append(Operation(kind=kind))

    return ops


Handler = Callable[[AVLTree[Any], Operation], tuple[str, list[Any]]]
# handler devuelve (mensaje, highlight_values)


def _h_insert(t: AVLTree[Any], op: Operation) -> tuple[str, list[Any]]:
    ok = t.insert(op.value)
    return (f"insert {op.value} → {'OK' if ok else 'YA EXISTE'}", [])


def _h_delete(t: AVLTree[Any], op: Operation) -> tuple[str, list[Any]]:
    ok = t.delete(op.value)
    return (f"delete {op.value} → {'OK' if ok else 'NO ENCONTRADO'}", [])


def _h_contains(t: AVLTree[Any], op: Operation) -> tuple[str, list[Any]]:
    ok = t.contains(op.value)
    trace = t.search_trace(op.value)
    return (f"contains {op.value} → {ok}", trace)


def _h_trace(t: AVLTree[Any], op: Operation) -> tuple[str, list[Any]]:
    trace = t.search_trace(op.value)
    found = bool(trace) and trace[-1] == op.value
    return (f"trace {op.value} → {'FOUND' if found else 'NOT FOUND'}", trace)


def _h_inorder(t: AVLTree[Any], _op: Operation) -> tuple[str, list[Any]]:
    return (f"inorder → {t.inorder()}", [])


def _h_bfs(t: AVLTree[Any], _op: Operation) -> tuple[str, list[Any]]:
    return (f"bfs → {t.bfs()}", [])


def _h_clear(t: AVLTree[Any], _op: Operation) -> tuple[str, list[Any]]:
    t.clear()
    return ("clear", [])


HANDLERS: dict[OpKind, Handler] = {
    OpKind.INSERT: _h_insert,
    OpKind.DELETE: _h_delete,
    OpKind.CONTAINS: _h_contains,
    OpKind.TRACE: _h_trace,
    OpKind.INORDER: _h_inorder,
    OpKind.BFS: _h_bfs,
    OpKind.CLEAR: _h_clear,
}


def build_steps(ops: list[Operation], *, dot_builder: callable) -> list[Step]:
    t: AVLTree[Any] = AVLTree()

    def snap(msg: str, hi: list[Any] | None = None) -> Step:
        return Step(
            dot=dot_builder(t.root, highlight=hi or []),
            inorder=t.inorder(),
            bfs=t.bfs(),
            height=t.height(),
            message=msg,
        )

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            msg, hi = HANDLERS[op.kind](t, op)
            steps.append(snap(msg, hi))
        except (ValueError, KeyError, IndexError) as e:
            steps.append(snap(f"ERROR: {e} (se detuvo la simulación)"))
            break

    return steps
